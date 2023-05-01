from django.test import TestCase
from auth_user.views import *
from auth_user.models import CustomAccount
import json


class TestBasic(TestCase):
    def test_create_account(self):
        # Test Correct Create Account
        response = self.client.post(
            path="http://127.0.0.1:8080/account/create",
            data=json.dumps(
                {
                    "email_address": "test2@test.com",
                    "password": "testpassword",
                    "first_name": "Test",
                    "last_name": "User",
                    "company": "Duck Creek",
                    "pay_rate": 10,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue("user_created" in response.json())

        # Test Create Existing Account
        response = self.client.post(
            path="http://127.0.0.1:8080/account/create",
            data=json.dumps(
                {
                    "email_address": "test2@test.com",
                    "password": "test",
                    "first_name": "User",
                    "last_name": "Name",
                    "company": "Duck Creek",
                    "pay_rate": 100,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)

        # Test Missing Data Feilds
        response = self.client.post(
            path="http://127.0.0.1:8080/account/create",
            data=json.dumps(
                {
                    "email_address": "test2@test.com",
                    "password": "test",
                    "first_name": "User",
                    "last_name": "Name",
                }
            ),
            content_type="application/json",
        )
        # Test Missing Email Address
        self.assertEqual(response.status_code, 401)
        response = self.client.post(
            path="http://127.0.0.1:8080/account/create",
            data=json.dumps(
                {
                    "password": "test",
                    "first_name": "User",
                    "last_name": "Name",
                    "company": "Duck Creek",
                    "pay_rate": 100,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)

    def test_login_verify(self):
        response = self.client.post(
            path="http://127.0.0.1:8080/account/create",
            data=json.dumps(
                {
                    "email_address": "test2@test.com",
                    "password": "testpassword",
                    "first_name": "Test",
                    "last_name": "User",
                    "company": "Duck Creek",
                    "pay_rate": 10,
                }
            ),
            content_type="application/json",
        )

        # Correct Login
        response = self.client.post(
            path="http://127.0.0.1:8080/account/login",
            data=json.dumps(
                {
                    "email_address": "test2@test.com",
                    "password": "testpassword",
                }
            ),
            content_type="application/json",
        )
        self.assertTrue(json.loads(response.content)["login_success"])
        TOKEN = json.loads(response.content)["token"]

        # Verify
        headers = {"HTTP_Authorization": f"Bearer {TOKEN}"}
        response = self.client.get(
            "http://127.0.0.1:8080/account/verify",
            **headers,
        )
        self.assertEqual(response.status_code, 200)

        # Verify no header
        headers = {}
        response = self.client.get(
            "http://127.0.0.1:8080/account/verify",
            **headers,
        )
        self.assertEqual(response.status_code, 401)

        # Incorrect Password
        response = self.client.post(
            path="http://127.0.0.1:8080/account/login",
            data=json.dumps(
                {
                    "email_address": "test2@test.com",
                    "password": "password",
                }
            ),
            content_type="application/json",
        )
        self.assertFalse(json.loads(response.content)["login_success"])
        self.assertEqual(response.status_code, 401)

        # Incorrect Email
        response = self.client.post(
            path="http://127.0.0.1:8080/account/login",
            data=json.dumps(
                {
                    "email_address": "wrong@test.com",
                    "password": "testpassword",
                }
            ),
            content_type="application/json",
        )
        self.assertFalse(json.loads(response.content)["login_success"])

    def test_employee(self):
        response = self.client.post(
            path="http://127.0.0.1:8080/account/create",
            data=json.dumps(
                {
                    "email_address": "employee1@test.com",
                    "password": "testpassword",
                    "first_name": "1",
                    "last_name": "User",
                    "company": "Duck Creek",
                    "pay_rate": 10,
                    "is_manager": False,
                }
            ),
            content_type="application/json",
        )

        response = self.client.post(
            path="http://127.0.0.1:8080/account/create",
            data=json.dumps(
                {
                    "email_address": "employee2@test.com",
                    "password": "testpassword",
                    "first_name": "2",
                    "last_name": "User",
                    "company": "Duck Creek",
                    "pay_rate": 100,
                    "is_manager": False,
                }
            ),
            content_type="application/json",
        )

        response = self.client.post(
            path="http://127.0.0.1:8080/account/create",
            data=json.dumps(
                {
                    "email_address": "manager@test.com",
                    "password": "testpassword",
                    "first_name": "Test",
                    "last_name": "User",
                    "company": "Duck Creek",
                    "pay_rate": 150,
                    "is_manager": True,
                }
            ),
            content_type="application/json",
        )

        response = self.client.post(
            path="http://127.0.0.1:8080/account/login",
            data=json.dumps(
                {
                    "email_address": "manager@test.com",
                    "password": "testpassword",
                }
            ),
            content_type="application/json",
        )
        TOKEN = json.loads(response.content)["token"]

        # Add Employee as Manager
        headers = {"HTTP_Authorization": f"Bearer {TOKEN}"}
        response = self.client.post(
            "http://127.0.0.1:8080/manager/add",
            **headers,
            data=json.dumps(
                {
                    "list_emails": ["employee1@test.com", "employee2@test.com"],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # Get Employee
        headers = {"HTTP_Authorization": f"Bearer {TOKEN}"}
        response = self.client.get(
            "http://127.0.0.1:8080/manager/get",
            **headers,
        )
        self.assertEqual(response.status_code, 200)

        # Remove Employee
        headers = {"HTTP_Authorization": f"Bearer {TOKEN}"}
        response = self.client.post(
            "http://127.0.0.1:8080/manager/remove",
            **headers,
            data=json.dumps(
                {
                    "list_emails": ["employee2@test.com"],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # Get Manager Pay
        headers = {"HTTP_Authorization": f"Bearer {TOKEN}"}
        response = self.client.get(
            "http://127.0.0.1:8080/employee/pay",
            **headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["pay_rate"], "150.00")

        # Set Manager Pay
        headers = {"HTTP_Authorization": f"Bearer {TOKEN}"}
        response = self.client.post(
            "http://127.0.0.1:8080/employee/pay",
            **headers,
            data=json.dumps(
                {
                    "pay_rate": 99,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)["user_modified"])

        # Set Manager Pay, missing fields
        headers = {"HTTP_Authorization": f"Bearer {TOKEN}"}
        response = self.client.post(
            "http://127.0.0.1:8080/employee/pay",
            **headers,
            data=json.dumps({}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 422)

        # Set Manager Pay, invalid pay rate format
        headers = {"HTTP_Authorization": f"Bearer {TOKEN}"}
        response = self.client.post(
            "http://127.0.0.1:8080/employee/pay",
            **headers,
            data=json.dumps(
                {
                    "pay_rate": "a string",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 422)

        # Test Incorrect Token
        headers = {"HTTP_Authorization": f"Bearer {1234}"}
        response = self.client.post(
            "http://127.0.0.1:8080/employee/pay",
            **headers,
            data=json.dumps(
                {
                    "pay_rate": 99,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            json.loads(response.content)["errors"], "Not Authenticated or Token invalid"
        )

        # Not as manager
        response = self.client.post(
            path="http://127.0.0.1:8080/account/login",
            data=json.dumps(
                {
                    "email_address": "employee1@test.com",
                    "password": "testpassword",
                }
            ),
            content_type="application/json",
        )
        TOKEN = json.loads(response.content)["token"]

        headers = {"HTTP_Authorization": f"Bearer {TOKEN}"}
        response = self.client.post(
            "http://127.0.0.1:8080/manager/add",
            **headers,
            data=json.dumps(
                {
                    "list_emails": ["employee1@test.com", "employee2@test.com"],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
