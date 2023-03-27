from django.test import TestCase
from auth_user.views import *
from auth_user.models import CustomAccount

class TestBasic(TestCase):
    
    def test_create_account_view(self):
        response = self.client.post(
            path='http://127.0.0.1:8080/account/create',
            data={
                "email_address": "test2@test.com",
                "password": "testpassword",
                "first_name": "Test",
                "last_name": "User",
                "company": "Duck Creek",
                "pay_rate": 10,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("user_created" in response.json())

    def test_create_account_existing(self):
        response = self.client.post(
            path='http://127.0.0.1:8080/account/create',
            data={
                "email_address": "test2@test.com",
                "password": "testpassword",
                "first_name": "Test",
                "last_name": "User",
                "company": "Duck Creek",
                "pay_rate": 10,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("user_created" in response.json())

        response = self.client.post(
            path='http://127.0.0.1:8080/account/create',
            data={
                "email_address": "test2@test.com",
                "password": "test",
                "first_name": "User",
                "last_name": "Name",
                "company": "Duck Creek",
                "pay_rate": 100,
            },
        )
        self.assertEqual(response.status_code, 500)
 