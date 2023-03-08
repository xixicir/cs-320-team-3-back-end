from auth_user.authentication import check_auth
from django.http import JsonResponse


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
