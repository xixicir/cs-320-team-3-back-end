"""timepunch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from auth_user.views import (
    CreateAccount,
    LoginAccount,
    VerifyAccount,
    AddEmployees,
    RemoveEmployees,
    GetEmployees,
)
from time_log.views import LogTime, GetTime, GetEmployeeTime

urlpatterns = [
    path("admin", admin.site.urls),
    path("account/create", CreateAccount.as_view()),
    path("account/login", LoginAccount.as_view()),
    path("account/verify", VerifyAccount.as_view()),
    path("manager/add", AddEmployees.as_view()),
    path("manager/remove", RemoveEmployees.as_view()),
    path("manager/get", GetEmployees.as_view()),
    path("time/log", LogTime.as_view()),
    path("time/get", GetTime.as_view()),
    path("time/employees", GetEmployeeTime.as_view()),
]
