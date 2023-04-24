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

from auth_user.views import auth_param


class LogTime(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'date_logged': openapi.Schema(type=openapi.TYPE_STRING, description="Date logged"),
            'num_hours': openapi.Schema(type=openapi.TYPE_STRING, description="Number of hours to be logged"),
            }),
        manual_parameters=[auth_param],
        responses={200: 'Success', 400: 'Bad Request'})
    @guarantee_auth
    def post(self, request, user: CustomAccount):
        request_params = request.data

        try:
            dt_logged = (
                date.today()
                if "date_logged" not in request_params
                else datetime.strptime(request_params["date_logged"], "%Y-%m-%d")
            )
        except ValueError:
            return JsonResponse(
                {
                    "log_created": False,
                    "errors": "date_logged is not in correct format (yyyy-mm-dd)",
                },
                status=500,
            )

        duplicate_logs = TimeEntry.objects.filter(user=user, date_logged=dt_logged)
        if duplicate_logs.exists():
            return JsonResponse(
                {
                    "log_created": False,
                    "errors": f"time log for date {dt_logged} already exists",
                },
                status=500,
            )

        if "num_hours" not in request_params:
            return JsonResponse(
                {
                    "log_created": False,
                    "errors": "num_hours not provided in request",
                },
                status=500,
            )

        cur_entry = TimeEntry(
            user=user,
            pay_rate=user.pay_rate,
            num_hours=request_params["num_hours"],
            date_logged=dt_logged,
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
        responses={200: 'Success', 400: 'Bad Request'})
    @guarantee_auth
    def get(self, request, user: CustomAccount):
        time_log = get_time_logs([user])[0]
        return JsonResponse(time_log, status=200)


class GetEmployeeTime(APIView):
    @swagger_auto_schema(
        manual_parameters=[auth_param],
        responses={200: 'Success', 400: 'Bad Request'})
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
                "pay_rates": list(map(lambda t: t.pay_rate, time_logs)),
                "date_logged": list(map(lambda t: t.date_logged, time_logs)),
                "num_hours": list(map(lambda t: t.num_hours, time_logs)),
            }
        )

    return list_info
