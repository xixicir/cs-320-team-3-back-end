from django.db import models
from auth_user.models import CustomAccount
from datetime import date


class TimeEntry(models.Model):
    user = models.ForeignKey(CustomAccount, on_delete=models.CASCADE)
    pay_rate = models.DecimalField(decimal_places=2, max_digits=10, default=25)
    date_logged = models.DateField(default=date.today)
    num_hours = models.IntegerField(default=8)
