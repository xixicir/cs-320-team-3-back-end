# Generated by Django 4.1.7 on 2023-03-27 19:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth_user", "0008_alter_customaccount_employee_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customaccount",
            name="employee_ID",
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
