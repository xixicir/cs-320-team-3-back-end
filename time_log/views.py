from typing import List

from django.http import JsonResponse
from auth_user.models import CustomAccount
from auth_user.utils import get_employees
from time_log.models import TimeEntry
from rest_framework.views import APIView
from auth_user.utils import guarantee_auth
from datetime import datetime, date
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from auth_user.views import auth_param, unauth_res


class LogTime(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "date_logged": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Date logged"
                ),
                "start": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Start time in iso format"
                ),
                "end": openapi.Schema(
                    type=openapi.TYPE_STRING, description="End time in iso format"
                ),
            },
        ),
        manual_parameters=[auth_param],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "log_created": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description="If the user was successfully created",
                    ),
                },
            ),
            500: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "log_created": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description="If the time log was successfully created",
                    ),
                    "errors": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            401: unauth_res,
        },
    )
    @guarantee_auth
    def post(self, request, user: CustomAccount):
        request_params = request.data

        try:
            start_dt = datetime.strptime(
                request_params["start"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            end_dt = datetime.strptime(request_params["end"], "%Y-%m-%dT%H:%M:%S.%fZ")

        except Exception:
            return JsonResponse(
                {
                    "log_created": False,
                    "errors": "The provided start and/or end time(s) are not in the correct format, please use: 'start' and 'end' (YYYY-MM-DDTHH:MM:SS.mmmZ)",
                },
                status=422,
            )

        if TimeEntry.objects.filter(start_time=start_dt, end_time=end_dt).exists():
            return JsonResponse(
                {
                    "log_created": False,
                    "errors": "The provided time range already has an entry in the database.",
                },
                status=422,
            )

        if start_dt >= end_dt:
            return JsonResponse(
                {
                    "log_created": False,
                    "errors": "The start time must be earlier than the end time.",
                },
                status=422,
            )

        cur_entry = TimeEntry(
            user=user,
            start_time=start_dt.isoformat(),
            end_time=end_dt.isoformat(),
            pay_rate=user.pay_rate,
        )
        cur_entry.save()

        return JsonResponse(
            {
                "log_created": True,
            },
            status=200,
        )


class GetTime(APIView):
    @swagger_auto_schema(
        manual_parameters=[auth_param],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "email": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Email of the user"
                    ),
                    "pay_rates": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                        description="Pay rates for each time log",
                    ),
                    "date_logged": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                        description="Dates for each time log",
                    ),
                    "num_hours": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                        description="Number of hours for each time log",
                    ),
                },
            ),
            401: unauth_res,
        },
    )
    @guarantee_auth
    def get(self, request, user: CustomAccount):
        time_log = get_time_logs([user])[0]
        return JsonResponse(time_log, status=200)


class GetEmployeeTime(APIView):
    @swagger_auto_schema(
        manual_parameters=[auth_param],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "email": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Email of the user"
                        ),
                        "pay_rates": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                            description="Pay rates for each time log",
                        ),
                        "date_logged": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                            description="Dates for each time log",
                        ),
                        "num_hours": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                            description="Number of hours for each time log",
                        ),
                    },
                ),
            ),
            401: unauth_res,
        },
    )
    @guarantee_auth
    def get(self, request, user: CustomAccount):
        time_logs = get_time_logs(get_employees(user))
        return JsonResponse(time_logs, status=200, safe=False)


def get_time_logs(list_users: List[CustomAccount]):
    list_info = []

    for user in list_users:
        time_logs = TimeEntry.objects.filter(user=user)

        list_info.append(
            {
                "email": user.email_address,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "time_entries": [
                    {
                        "pay_rate": t.pay_rate,
                        "start": t.start_time,
                        "end": t.end_time,
                    }
                    for t in time_logs
                ],
            }
        )

    return list_info
