from django.contrib import admin
from auth_user.models import CustomAccount
from time_log.models import TimeEntry

admin.site.register(CustomAccount)
admin.site.register(TimeEntry)
