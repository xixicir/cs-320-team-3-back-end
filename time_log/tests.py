from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from auth_user.models import CustomAccount
from time_log.models import TimeEntry
from datetime import date, datetime
from rest_framework.authtoken.models import Token
import json


class TestLogs(TestCase):
    def test_create_time_log_success(self):
        url = "http://127.0.0.1:8080/time/log"
        data = {
            "num_hours": 8,
            "date_logged": str(date.today()),
        }
        user_data = {
            "email_address": "testusertime@example.com",
            "password": "password123",
            "company": "Test Company",
            "first_name": "Test",
            "last_name": "User",
        }
        response = self.client.post(
            path="http://127.0.0.1:8080/account/create",
            data=json.dumps(user_data),
            content_type="application/json",
        )

        user = CustomAccount.objects.get(email_address=user_data["email_address"])

        TOKEN = json.loads(response.content)["token"]
        headers = {"HTTP_Authorization": f"Bearer {TOKEN}"}

        # Log Time
        response = self.client.post(
            url, json.dumps(data), content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            TimeEntry.objects.filter(
                user=user, num_hours=8, date_logged=date.today()
            ).exists()
        )
        self.assertEqual(json.loads(response.content)["log_created"], True)

        # Get Time
        url = "http://127.0.0.1:8080/time/get"
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 200)

        t_entries = response.json().get("time_entries", [])
        self.assertTrue(
            len(t_entries) == 1 and t_entries[0]["date_logged"] == data["date_logged"]
        )

        # Log Time again
        response = self.client.post(
            "http://127.0.0.1:8080/time/log",
            json.dumps(data),
            content_type="application/json",
            **headers,
        )
        self.assertEqual(response.status_code, 422)
