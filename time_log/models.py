from django.db import models
from auth_user.models import CustomAccount

# Create your models here.

# TODO -> add time field and create API calls for creating / fetching logs
class WorkEntry(models.Model):
    user = models.ForeignKey(CustomAccount, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.TimeField()

