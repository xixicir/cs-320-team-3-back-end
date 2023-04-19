from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from auth_user.models import CustomAccount
from time_log.models import TimeEntry
from datetime import date, datetime
from rest_framework.authtoken.models import Token
import json

class TestLogs(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            "email_address": "testuser@example.com",
            "password": "password123",
            "company": "Test Company",
            "first_name": "Test",
            "last_name": "User",
        }
        response = self.client.post('http://127.0.0.1:8080/account/create', data=self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user_created'], True)
        self.user = CustomAccount.objects.get(email_address=self.user_data['email_address'])
        self.token = Token.objects.get(user=self.user)

    def test_create_time_log_success(self):
        url = "http://127.0.0.1:8080/time/log"
        data = {
            'num_hours': 8,
            'date_logged': str(date.today()),
        }
        response = self.client.post(
            path='http://127.0.0.1:8080/account/login',
            data={
                "email_address": "testuser@example.com",
                "password": "password123",
            }
        )
        print(response)
        TOKEN = json.loads(response.content)['token']
        headers={
            "HTTP_Authorization": f"Bearer {TOKEN}"
        }

        # Log Time
        response = self.client.post(url, data, format='json',**headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(TimeEntry.objects.filter(user=self.user, num_hours=8, date_logged=date.today()).exists())
        self.assertEqual(json.loads(response.content)['log_created'], True)

        # # Get Time
        # url = "http://127.0.0.1:8080/time/get"
        # response = self.client.get(url, self.user)
        # self.assertEqual(response.status_code, 200)
        # # print(response.time_log)

