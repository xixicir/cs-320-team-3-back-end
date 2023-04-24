from django.db import models
from django.contrib.auth.models import AbstractUser
from auth_user.managers import CustomUserManager
from django.utils import timezone
from rest_framework import serializers


class CustomAccount(AbstractUser):
    username = None
    company = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_manager = models.BooleanField(default=False)

    start_date = models.DateField(default=timezone.now)

    employee_ID = models.IntegerField(null=True, blank=True)
    company_ID = models.IntegerField(default=0)
    position = models.CharField(max_length=50, default="employee")

    manager = models.ForeignKey(
        "CustomAccount", on_delete=models.CASCADE, blank=True, null=True
    )
    email_address = models.EmailField(max_length=50, unique=True)
    pay_rate = models.DecimalField(decimal_places=2, max_digits=10, default=25)

    objects = CustomUserManager()
    USERNAME_FIELD = "email_address"
    REQUIRED_FIELDS = ["company", "first_name", "last_name"]


class CustomAccountSerializer(serializers.Serializer):
    company = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    is_manager = serializers.BooleanField(default=False)

    start_date = serializers.DateField()

    employee_ID = serializers.IntegerField()
    company_ID = serializers.IntegerField(default=0)
    position = serializers.CharField(max_length=50, default="employee")

    manager_name = serializers.RelatedField(
        source="manager", read_only=True
    )

    email_address = serializers.EmailField(max_length=50)
    pay_rate = serializers.DecimalField(decimal_places=2, max_digits=10, default=25)

