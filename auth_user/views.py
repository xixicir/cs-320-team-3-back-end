from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from auth_user.models import CustomAccount
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
import json
from auth_user.utils import guarantee_auth, get_employees
from functools import reduce
import operator
from django.db.models import Q


class CreateAccount(APIView):
    def post(self, request):
        request_params = request.POST.dict()
        try:
            duplicate_users = CustomAccount.objects.filter(
                email_address=request_params["email_address"]
            )
            if duplicate_users.exists():
                return JsonResponse(
                    {
                        "user_created": False,
                        "errors": "email address already exists",
                    },
                    status=500,
                )

            this_user = CustomAccount.objects.create_user(**request_params)
            token_object = Token.objects.create(user=this_user)
            return JsonResponse(
                {
                    "user_created": True,
                    "token": token_object.key,
                }
            )
        except KeyError as e:
            return JsonResponse(
                {"user_created": False, "errors": f"BadRequest: Missing key\n{e}"},
                status=500,
            )


class LoginAccount(APIView):
    def post(self, request):
        request_params = request.POST.dict()
        user = authenticate(**request_params)
        if user:
            login(request, user)
            Token.objects.filter(user_id=user.id).delete()  # delete old entry if exists
            token_object = Token.objects.create(user=user)
            return JsonResponse(
                {
                    "login_success": True,
                    "token": token_object.key,
                }
            )
        else:
            # Return an 'invalid login' error message.
            return JsonResponse(
                {
                    "login_success": False,
                    "errors": "email or password invalid",
                },
                status=500,
            )


class VerifyAccount(APIView):
    @guarantee_auth
    def get(self, request, user):
        return JsonResponse(
            {
                "login_success": True,
            },
            status=200,
        )


class AddEmployees(APIView):
    @guarantee_auth
    def post(self, request, user: CustomAccount):
        request_params = request.POST.dict()
        return map_users(request_params, user)


class RemoveEmployees(APIView):
    @guarantee_auth
    def post(self, request, user: CustomAccount):
        request_params = request.POST.dict()
        return map_users(request_params, None)


class GetEmployees(APIView):
    @guarantee_auth
    def get(self, request, user: CustomAccount):
        list_employees = get_employees(user)

        return JsonResponse(
            {
                "list_employees": list(map(lambda u: u.email_address, list_employees)),
            },
            status=200,
        )


def map_users(request_params, val):
    list_emails = json.loads(request_params.get("list_emails", "[]"))
    if not list_emails:
        return JsonResponse(
            {
                "success": False,
                "errors": "No list_emails field in request"
            },
            status=500,
        )

    # TODO: add filter for company
    list_possible: [CustomAccount] = CustomAccount.objects.filter(
        reduce(operator.or_, (Q(email_address__contains=x) for x in list_emails))
    )

    for employee in list_possible:
        employee.manager = val
        employee.save()

    return JsonResponse(
        {
            "success": True,
        },
        status=200,
    )
