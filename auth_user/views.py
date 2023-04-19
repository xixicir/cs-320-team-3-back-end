from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from auth_user.models import CustomAccount
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
import json
from auth_user.utils import guarantee_auth, get_employees
from functools import reduce
import operator
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.forms.models import model_to_dict


class CreateAccount(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email_address": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Email address"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Password"
                ),
                "pay_rate": openapi.Schema(
                    type=openapi.TYPE_NUMBER, description="Pay rate per hour"
                ),
                "company": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Company"
                ),
                "first_name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="First name"
                ),
                "last_name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Last name"
                ),
            },
        ),
        responses={200: "Success", 400: "Bad Request"},
    )
    def post(self, request):
        request_params = request.data
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
                    status=401,
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
                status=401,
            )


class LoginAccount(APIView):
    def post(self, request):
        request_params = request.data
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
                status=401,
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


class GetAccount(APIView):
    @guarantee_auth
    def get(self, request, user):
        dict_user = model_to_dict(user, exclude=["password"])
        return JsonResponse(
            dict_user,
            status=200,
        )


class AddEmployees(APIView):
    @guarantee_auth
    def post(self, request, user: CustomAccount):
        request_params = request.data
        return map_users(request_params, user, is_removed=False)


class RemoveEmployees(APIView):
    @guarantee_auth
    def post(self, request, user: CustomAccount):
        request_params = request.data
        return map_users(request_params, user, is_removed=True)


class GetEmployees(APIView):
    @guarantee_auth
    def get(self, request, user: CustomAccount):
        list_employees = get_employees(user)

        return JsonResponse(
            {
                "list_employees": list(
                    map(
                        lambda u: model_to_dict(u, exclude=["password"]), list_employees
                    )
                ),
            },
            status=200,
        )


def map_users(request_params, val, is_removed):
    list_emails = request_params.get("list_emails", "[]")
    if not list_emails:
        return JsonResponse(
            {"success": False, "errors": "No list_emails field in request"},
            status=422,
        )
    try:
        list_possible: [CustomAccount] = CustomAccount.objects.filter(
            reduce(operator.or_, (Q(email_address__contains=x) for x in list_emails))
        ).filter(Q(company=val.company))
    except:
        return JsonResponse(
            {"success": False, "errors": "Error Filtering Company"},
            status=400,
        )

    for employee in list_possible:
        if not is_removed:
            employee.manager = val
        else:
            employee.manager = None
        employee.save()

    return JsonResponse(
        {
            "success": True,
        },
        status=200,
    )


# allows for both getting pay and setting pay
class EmployeePay(APIView):
    @guarantee_auth
    def get(self, request, user: CustomAccount):
        return JsonResponse(
            {
                "pay_rate": user.pay_rate,
            },
            status=200,
        )

    @guarantee_auth
    def post(self, request, user: CustomAccount):
        params = request.POST.dict()
        if "pay_rate" not in params:
            return JsonResponse(
                {
                    "user_modified": False,
                    "errors": "pay_rate is missing",
                },
                status=422,
            )
        try:
            user.pay_rate = params["pay_rate"]
            user.clean_fields()
            user.save()
        except ValidationError:
            return JsonResponse(
                {
                    "user_modified": False,
                    "errors": "pay_rate is not a valid float with two decimal places maximum",
                },
                status=422,
            )
        return JsonResponse(
            {
                "user_modified": True,
            },
            status=200,
        )
