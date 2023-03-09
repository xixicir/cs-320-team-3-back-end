from typing import List

from django.http import JsonResponse
from auth_user.models import CustomAccount
from auth_user.utils import get_employees
from time_log.models import TimeEntry
from rest_framework.views import APIView
from auth_user.utils import guarantee_auth
from datetime import date


class LogTime(APIView):
    @guarantee_auth
    def post(self, request, user: CustomAccount):
        duplicate_logs = TimeEntry.objects.filter(
            user=user,
            date_logged=date.today()
        )
        if duplicate_logs.exists():
            return JsonResponse(
                {
                    "log_created": False,
                    "errors": "time log for today already exists",
                },
                status=500,
            )

        request_params = request.POST.dict()
        if "num_hours" not in request_params:
            return JsonResponse(
                {
                    "log_created": False,
                    "errors": "num_hours not provided in request",
                },
                status=500,
            )

        cur_entry = TimeEntry(user=user, pay_rate=user.pay_rate, num_hours=request_params["num_hours"])
        cur_entry.save()

        return JsonResponse(
            {
                "log_created": True,

            },
            status=200,
        )


class GetTime(APIView):
    @guarantee_auth
    def get(self, request, user: CustomAccount):
        time_log = get_time_logs([user])[0]
        return JsonResponse(time_log, status=200)


class GetEmployeeTime(APIView):
    @guarantee_auth
    def get(self, request, user: CustomAccount):
        time_logs = get_time_logs(get_employees(user))
        return JsonResponse(time_logs, status=200, safe=False)


def get_time_logs(list_users: List[CustomAccount]):
    list_info = []

    for user in list_users:
        time_logs = TimeEntry.objects.filter(
            user=user
        )

        # TODO: optimize this
        list_info.append({
            "email": user.email_address,
            "pay_rates": list(map(lambda t: t.pay_rate, time_logs)),
            "date_logged": list(map(lambda t: t.date_logged, time_logs)),
            "num_hours": list(map(lambda t: t.num_hours, time_logs)),
        })

    return list_info

