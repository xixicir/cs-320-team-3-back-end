from django.db import models
from auth_user.models import CustomAccount


class TimeEntry(models.Model):
    user = models.ForeignKey(CustomAccount, on_delete=models.CASCADE)
    pay_rate = models.DecimalField(decimal_places=2, max_digits=5, default=25)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
