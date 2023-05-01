from django.test import TestCase
from auth_user.models import CustomAccount
from time_log.models import TimeEntry
from datetime import date, datetime
import json
from datetime import timedelta


class TestLogs(TestCase):
    def test_create_time_log_success(self):
        url = "http://127.0.0.1:8080/time/log"

        dt_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        dt_now = datetime.now()
        start_dt = dt_now.strftime(dt_format)
        end_dt = (dt_now + timedelta(hours=8)).strftime(dt_format)

        data = {"start": start_dt, "end": end_dt}

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

        # Log Time, invalid format
        response = self.client.post(
            url, json.dumps({
                "start": "asdf",
                "end": "asdf",
            }), content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 422)

        # Log Time, time out of order
        response = self.client.post(
            url, json.dumps({
                "start": end_dt,
                "end": start_dt,
            }), content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 422)

        # Log Time
        response = self.client.post(
            url, json.dumps(data), content_type="application/json", **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(TimeEntry.objects.filter(user=user, start_time=dt_now).exists())
        self.assertEqual(json.loads(response.content)["log_created"], True)

        # Get Time
        url = "http://127.0.0.1:8080/time/get"
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 200)

        t_entries = response.json().get("time_entries", [])
        self.assertTrue(
            len(t_entries) == 1
            and t_entries[0]["start"].split("T")[0] == data["start"].split("T")[0]
        )

        # Log Time again
        response = self.client.post(
            "http://127.0.0.1:8080/time/log",
            json.dumps(data),
            content_type="application/json",
            **headers,
        )
        self.assertEqual(response.status_code, 422)
