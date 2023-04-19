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
from django.core.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.forms.models import model_to_dict

# note: default value is a token that exists in my own database. change this
#   for making testing with swagger faster as necessary
auth_param = openapi.Parameter(
        name="Authorization",
        type=openapi.TYPE_STRING,
        in_="header",
        required=True,
        description='Token for authentication. Include the \"Bearer\" in the beginning',
        default="Bearer 23fd9369a5a1f32e1b907c6a84620c10c09706ec")

unauth_res = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'errors': openapi.Schema(
            type=openapi.TYPE_STRING),
    },
    description='Error response for unauthorized access')


class CreateAccount(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email_address': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Email address',
                    default='john.doe@gmail.com'),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Password',
                    default='passwordThis123'),
                'pay_rate': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='Pay rate per hour',
                    default=45),
                'company': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Company',
                    default='google'),
                'first_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='First name',
                    default='John'),
                'last_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Last name',
                    default='Doe'),
            }),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user_created': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description='If the user was successfully created'),
                    'token': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='A token for the user just created'),
                }),
            500: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user_created': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description='If the user was successfully created'),
                    'errors': openapi.Schema(type=openapi.TYPE_STRING),
                }),
            })
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
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email_address': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Email address',
                    default="john.doe@gmail.com"),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Password',
                    default="passwordThis123"),
            }),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'login_success': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description='If logged in successfully'),
                    'token': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='A token for the user specified'),
                }),
            500: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'login_success': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description='If logged in successfully'),
                    'errors': openapi.Schema(type=openapi.TYPE_STRING),
                }),
            },
        )
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
    @swagger_auto_schema(
        manual_parameters=[auth_param],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'login_success': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description='If logged in successfully'),
                }),
            401: unauth_res},
        )

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
    @swagger_auto_schema(request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'list_emails': openapi.Schema(name="email list",
                                      type=openapi.TYPE_ARRAY,
                                      items=openapi.Schema(type=openapi.TYPE_STRING), 
                                      description='Email List',
                                      default=['john.doe@gmail.com']),
        }),
    manual_parameters=[auth_param],
    responses={200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description="if added the employees successfully",
                        default=True
                        )
                }), 500: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description="if there is no list_emails field in request or invalid company",
                        default=False
                        ),
                    "errors" : openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="error messages"
                    )
                })})
    @guarantee_auth
    def post(self, request, user: CustomAccount):
        request_params = request.data
        return map_users(request_params, user, is_removed=False)


class RemoveEmployees(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'list_emails': openapi.Schema(type=openapi.TYPE_ARRAY,
                                      items=openapi.Schema(type=openapi.TYPE_STRING), 
                                      description='Email List',
                                      default=['john.doe@gmail.com']),
        }),
    manual_parameters=[auth_param],
    responses={200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description="if remove the employees successfully",
                        default=True
                        )
                }), 500: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description="if there is no list_emails field in request or invalid company",
                        default=False
                        ),
                    "errors" : openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="error messages"
                    )
                })})
    @guarantee_auth
    def post(self, request, user: CustomAccount):
        request_params = request.data
        return map_users(request_params, user, is_removed=True)


class GetEmployees(APIView):
    @swagger_auto_schema(
    manual_parameters=[auth_param],
    responses={200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'list_employees': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_STRING
                        ),description="list of employees under the user"
                        )
                },description='If logged in successfully'), 400: 'Bad Request'})
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
    list_emails = request_params.get("list_emails", [])
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
    @swagger_auto_schema(
        manual_parameters=[auth_param],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'pay_rate': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description='Pay rate of the user'),
                }),
            401: unauth_res},
        )
    @guarantee_auth
    def get(self, request, user: CustomAccount):
        return JsonResponse(
            {
                "pay_rate": user.pay_rate,
            },
        )

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'pay_rate': openapi.Schema(type=openapi.TYPE_STRING, description='Pay rate'),
            }),
        manual_parameters=[auth_param],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user_modified': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description='If the user was successfully modified'),
                }),
            500: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user_modified': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description='If the user was successfully modified'),
                    'errors': openapi.Schema(type=openapi.TYPE_STRING),
                }),
            401: unauth_res},
        )
    @guarantee_auth
    def post(self, request, user: CustomAccount):
        params = request.data
        if "pay_rate" not in params:
            return JsonResponse(
                {
                    "user_modified": False,
                    "errors": "missing field pay_rate",
                },
                status=422,
            )

        if not isinstance(params["pay_rate"], (int, float)):
            return JsonResponse(
                {
                    "user_modified": False,
                    "errors": "pay_rate is not a valid float with two decimal places maximum",
                },
                status=422,
            )
        user.pay_rate = round(params["pay_rate"], 2)
        user.save()
        return JsonResponse(
            {
                "user_modified": True,
            },
        )
