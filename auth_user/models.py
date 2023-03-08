from django.db import models
from django.contrib.auth.models import AbstractUser
from auth_user.managers import CustomUserManager


class CustomAccount(AbstractUser):
    username = None
    company = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    manager = models.ForeignKey('CustomAccount', on_delete=models.CASCADE, blank=True, null=True)
    email_address = models.EmailField(max_length=50, unique=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "email_address"
    REQUIRED_FIELDS = ["company", "first_name", "last_name"]
