# Generated by Django 4.1.7 on 2023-04-03 18:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth_user", "0009_alter_customaccount_employee_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customaccount",
            name="employee_ID",
            field=models.IntegerField(null=True),
        ),
    ]
