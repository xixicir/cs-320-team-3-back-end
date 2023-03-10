from typing import List

from auth_user.authentication import check_auth
from django.http import JsonResponse
from auth_user.models import CustomAccount


def guarantee_auth(f):
    def check_for_auth(*args):
        success, user, _ = check_auth(args[1])
        if not success:
            return JsonResponse(
                {
                    "errors": "Not Authenticated or Token invalid",
                },
                status=401,
            )

        else:
            return f(*args, user=user)

    return check_for_auth


# TODO: account for transitive (get employees of employees)
def get_employees(user) -> List[CustomAccount]:
    return CustomAccount.objects.filter(manager=user)
