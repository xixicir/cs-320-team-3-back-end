from typing import List
from auth_user.authentication import check_auth
from django.http import JsonResponse
from auth_user.models import CustomAccount


def guarantee_auth(f):
    def check_for_auth(*args):
        params = args[1].data
        if "email_address" not in params:
            return JsonResponse(
                {
                    "errors": "Not Authenticated or Token invalid",
                },
                status=401,
            )
        else:
            try:
                user = CustomAccount.objects.get(email_address=params["email_address"])
            except Exception:
                return JsonResponse(
                    {
                        "errors": "user does not exist",
                    },
                    status=404,
                )
            return f(*args, user=user)

    return check_for_auth


def get_employees(user) -> List[CustomAccount]:
    list_init = [user]
    list_employees = []

    while list_init:
        cur_user = list_init.pop()
        cur_employees = CustomAccount.objects.filter(manager=cur_user)
        list_employees.extend(cur_employees)
        list_init.extend(cur_employees)

    return list_employees
