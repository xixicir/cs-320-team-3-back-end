from django.test import TestCase
from auth_user.views import *
from auth_user.models import CustomAccount
import json


class TestBasic(TestCase):
<<<<<<< HEAD

    def test_create_account(self):
        # Test Correct Create Account
||||||| parent of f356d56 (Formatting)
    
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
=======
    def test_create_account_view(self):
        response = self.client.post(
            path="http://127.0.0.1:8080/account/create",
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

<<<<<<< HEAD
    def test_create_account_existing(self):
>>>>>>> f356d56 (Formatting)
||||||| parent of c044538 (small changes)
    def test_create_account_existing(self):
=======
    def test_create_account_view(self):
>>>>>>> c044538 (small changes)
        response = self.client.post(
            path="http://127.0.0.1:8080/account/create",
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

<<<<<<< HEAD
        # Test Create Existing Account
||||||| parent of c044538 (small changes)
=======

    def test_create_account(self):
        # Test Correct Create Account
        response = self.client.post(
            path="http://127.0.0.1:8080/account/create",
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

        # Test Create Existing Account
>>>>>>> c044538 (small changes)
        response = self.client.post(
            path="http://127.0.0.1:8080/account/create",
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
<<<<<<< HEAD
<<<<<<< HEAD

        # Test Missing Data Feilds
        response = self.client.post(
            path='http://127.0.0.1:8080/account/create',
            data={
                "email_address": "test2@test.com",
                "password": "test",
                "first_name": "User",
                "last_name": "Name",
            },
        )
        self.assertEqual(response.status_code, 500)
 
    def test_login_verify(self):
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

        # Correct Login
        response = self.client.post(
            path='http://127.0.0.1:8080/account/login',
            data={
                "email_address": "test2@test.com",
                "password": "testpassword",
            },
        )
        self.assertTrue(json.loads(response.content)['login_success'])
        TOKEN = json.loads(response.content)['token']

        # Verify 
        headers={
            "HTTP_Authorization": f"Bearer {TOKEN}"
        }
        response = self.client.get(
            'http://127.0.0.1:8080/account/verify',
            **headers,
        )
        self.assertEqual(response.status_code, 200)

        # Incorrect Password
        response = self.client.post(
            path='http://127.0.0.1:8080/account/login',
            data={
                "email_address": "test2@test.com",
                "password": "password",
            },
        )
        self.assertFalse(json.loads(response.content)['login_success'])
        self.assertEqual(response.status_code, 500)

        # Incorrect Email
        response = self.client.post(
            path='http://127.0.0.1:8080/account/login',
            data={
                "email_address": "wrong@test.com",
                "password": "testpassword",
            },
        )
        self.assertFalse(json.loads(response.content)['login_success'])

    def test_employee(self):
        response = self.client.post(
            path='http://127.0.0.1:8080/account/create',
            data={
                "email_address": "employee1@test.com",
                "password": "testpassword",
                "first_name": "1",
                "last_name": "User",
                "company": "Duck Creek",
                "pay_rate": 10,
                "is_manager": False,
            },
        )

        response = self.client.post(
            path='http://127.0.0.1:8080/account/create',
            data={
                "email_address": "employee2@test.com",
                "password": "testpassword",
                "first_name": "2",
                "last_name": "User",
                "company": "Duck Creek",
                "pay_rate": 100,
                "is_manager": False,
            },
        )
        
        response = self.client.post(
            path='http://127.0.0.1:8080/account/create',
            data={
                "email_address": "manager@test.com",
                "password": "testpassword",
                "first_name": "Test",
                "last_name": "User",
                "company": "Duck Creek",
                "pay_rate": 150,
                "is_manager": True,
            },
        )

        response = self.client.post(
            path='http://127.0.0.1:8080/account/login',
            data={
                "email_address": "manager@test.com",
                "password": "testpassword",
            },
        )
        TOKEN = json.loads(response.content)['token']

        # Add Employee as Manager
        headers={
            "HTTP_Authorization": f"Bearer {TOKEN}"
        }
        response = self.client.post(
            'http://127.0.0.1:8080/manager/add',
            **headers,
            data={
                "list_emails": '["employee1@test.com", "employee2@test.com"]',
            }
        )
        self.assertEqual(response.status_code, 200)

        # Get Employee
        headers={
            "HTTP_Authorization": f"Bearer {TOKEN}"
        }
        response = self.client.get(
            'http://127.0.0.1:8080/manager/get',
            **headers,
        )
        self.assertEqual(response.status_code, 200)

        # Remove Employee
        headers={
            "HTTP_Authorization": f"Bearer {TOKEN}"
        }
        response = self.client.post(
            'http://127.0.0.1:8080/manager/remove',
            **headers,
            data={
                "list_emails": '["employee2@test.com"]',
            }
        )
        self.assertEqual(response.status_code, 200)

        # Get Manager Pay
        headers={
            "HTTP_Authorization": f"Bearer {TOKEN}"
        }
        response = self.client.get(
            'http://127.0.0.1:8080/employee/pay',
            **headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['pay_rate'], '150.00')

        # Set Manager Pay
        headers={
            "HTTP_Authorization": f"Bearer {TOKEN}"
        }
        response = self.client.post(
            'http://127.0.0.1:8080/employee/pay',
            **headers,
            data={
                'pay_rate' : 99,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['user_modified'])

        # Test Incorrect Token
        headers={
            "HTTP_Authorization": f"Bearer {1234}"
        }
        response = self.client.post(
            'http://127.0.0.1:8080/employee/pay',
            **headers,
            data={
                'pay_rate' : 99,
            },
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content)['errors'], "Not Authenticated or Token invalid")

        # Not as manager 
        response = self.client.post(
            path='http://127.0.0.1:8080/account/login',
            data={
                "email_address": "employee1@test.com",
                "password": "testpassword",
            },
        )
        TOKEN = json.loads(response.content)['token']

        headers={
            "HTTP_Authorization": f"Bearer {TOKEN}"
        }
        response = self.client.post(
            'http://127.0.0.1:8080/manager/add',
            **headers,
            data={
                "list_emails": '["employee1@test.com", "employee2@test.com"]',
            }
        )
        self.assertEqual(response.status_code, 200)
||||||| parent of f356d56 (Formatting)
 
=======
>>>>>>> f356d56 (Formatting)
||||||| parent of c044538 (small changes)
=======

        # Test Missing Data Feilds
        response = self.client.post(
            path='http://127.0.0.1:8080/account/create',
            data={
                "email_address": "test2@test.com",
                "password": "test",
                "first_name": "User",
                "last_name": "Name",
            },
        )
        self.assertEqual(response.status_code, 500)
 
    def test_login_verify(self):
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

        # Correct Login
        response = self.client.post(
            path='http://127.0.0.1:8080/account/login',
            data={
                "email_address": "test2@test.com",
                "password": "testpassword",
            },
        )
        self.assertTrue(json.loads(response.content)['login_success'])
        TOKEN = json.loads(response.content)['token']

        # Verify 
        headers={
            "HTTP_Authorization": f"Bearer {TOKEN}"
        }
        response = self.client.get(
            'http://127.0.0.1:8080/account/verify',
            **headers,
        )
        self.assertEqual(response.status_code, 200)

        # Incorrect Password
        response = self.client.post(
            path='http://127.0.0.1:8080/account/login',
            data={
                "email_address": "test2@test.com",
                "password": "password",
            },
        )
        self.assertFalse(json.loads(response.content)['login_success'])
        self.assertEqual(response.status_code, 500)

        # Incorrect Email
        response = self.client.post(
            path='http://127.0.0.1:8080/account/login',
            data={
                "email_address": "wrong@test.com",
                "password": "testpassword",
            },
        )
        self.assertFalse(json.loads(response.content)['login_success'])

    def test_employee(self):
        response = self.client.post(
            path='http://127.0.0.1:8080/account/create',
            data={
                "email_address": "employee1@test.com",
                "password": "testpassword",
                "first_name": "1",
                "last_name": "User",
                "company": "Duck Creek",
                "pay_rate": 10,
                "is_manager": False,
            },
        )

        response = self.client.post(
            path='http://127.0.0.1:8080/account/create',
            data={
                "email_address": "employee2@test.com",
                "password": "testpassword",
                "first_name": "2",
                "last_name": "User",
                "company": "Duck Creek",
                "pay_rate": 100,
                "is_manager": False,
            },
        )
        
        response = self.client.post(
            path='http://127.0.0.1:8080/account/create',
            data={
                "email_address": "manager@test.com",
                "password": "testpassword",
                "first_name": "Test",
                "last_name": "User",
                "company": "Duck Creek",
                "pay_rate": 150,
                "is_manager": True,
            },
        )

        response = self.client.post(
            path='http://127.0.0.1:8080/account/login',
            data={
                "email_address": "manager@test.com",
                "password": "testpassword",
            },
        )
        TOKEN = json.loads(response.content)['token']

        # Add Employee as Manager
        headers={
            "HTTP_Authorization": f"Bearer {TOKEN}"
        }
        response = self.client.post(
            'http://127.0.0.1:8080/manager/add',
            **headers,
            data={
                "list_emails": '["employee1@test.com", "employee2@test.com"]',
            }
        )
        self.assertEqual(response.status_code, 200)

        # Get Employee
        headers={
            "HTTP_Authorization": f"Bearer {TOKEN}"
        }
        response = self.client.get(
            'http://127.0.0.1:8080/manager/get',
            **headers,
        )
        self.assertEqual(response.status_code, 200)

        # Remove Employee
        headers={
            "HTTP_Authorization": f"Bearer {TOKEN}"
        }
        response = self.client.post(
            'http://127.0.0.1:8080/manager/remove',
            **headers,
            data={
                "list_emails": '["employee2@test.com"]',
            }
        )
        self.assertEqual(response.status_code, 200)

        # Get Manager Pay
        headers={
            "HTTP_Authorization": f"Bearer {TOKEN}"
        }
        response = self.client.get(
            'http://127.0.0.1:8080/employee/pay',
            **headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['pay_rate'], '150.00')

        # Set Manager Pay
        headers={
            "HTTP_Authorization": f"Bearer {TOKEN}"
        }
        response = self.client.post(
            'http://127.0.0.1:8080/employee/pay',
            **headers,
            data={
                'pay_rate' : 99,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['user_modified'])

        # Test Incorrect Token
        headers={
            "HTTP_Authorization": f"Bearer {1234}"
        }
        response = self.client.post(
            'http://127.0.0.1:8080/employee/pay',
            **headers,
            data={
                'pay_rate' : 99,
            },
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content)['errors'], "Not Authenticated or Token invalid")

        # Not as manager 
        response = self.client.post(
            path='http://127.0.0.1:8080/account/login',
            data={
                "email_address": "employee1@test.com",
                "password": "testpassword",
            },
        )
        TOKEN = json.loads(response.content)['token']

        headers={
            "HTTP_Authorization": f"Bearer {TOKEN}"
        }
        response = self.client.post(
            'http://127.0.0.1:8080/manager/add',
            **headers,
            data={
                "list_emails": '["employee1@test.com", "employee2@test.com"]',
            }
        )
        self.assertEqual(response.status_code, 200)

        # Test Missing Data Feilds
        response = self.client.post(
            path='http://127.0.0.1:8080/account/create',
            data={
                "email_address": "test2@test.com",
                "password": "test",
                "first_name": "User",
                "last_name": "Name",
            },
        )
        self.assertEqual(response.status_code, 500)
 
    def test_login_verify(self):
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

        # Correct Login
        response = self.client.post(
            path='http://127.0.0.1:8080/account/login',
            data={
                "email_address": "test2@test.com",
                "password": "testpassword",
            },
        )
        self.assertTrue(json.loads(response.content)['login_success'])
        TOKEN = json.loads(response.content)['token']

        # Verify 
        response = self.client.get(
            path='http://127.0.0.1:8080/account/verify',
            headers={
                "Authorization": f"Bearer {TOKEN}"
            },
        )
        self.assertEqual(response.status_code, 200)


        # Incorrect Password
        response = self.client.post(
            path='http://127.0.0.1:8080/account/login',
            data={
                "email_address": "test2@test.com",
                "password": "password",
            },
        )
        self.assertFalse(json.loads(response.content)['login_success'])

        # Incorrect Email
        response = self.client.post(
            path='http://127.0.0.1:8080/account/login',
            data={
                "email_address": "wrong@test.com",
                "password": "testpassword",
            },
        )
        self.assertFalse(json.loads(response.content)['login_success'])

    # def test_employee(self):
    #     response = self.client.post(
    #         path='http://127.0.0.1:8080/account/create',
    #         data={
    #             "email_address": "employee1@test.com",
    #             "password": "testpassword",
    #             "first_name": "1",
    #             "last_name": "User",
    #             "company": "Duck Creek",
    #             "pay_rate": 10,
    #             "is_manager": False,
    #         },
    #     )

    #     response = self.client.post(
    #         path='http://127.0.0.1:8080/account/create',
    #         data={
    #             "email_address": "employee2@test.com",
    #             "password": "testpassword",
    #             "first_name": "2",
    #             "last_name": "User",
    #             "company": "Duck Creek",
    #             "pay_rate": 10,
    #             "is_manager": False,
    #         },
    #     )
        
    #     response = self.client.post(
    #         path='http://127.0.0.1:8080/account/create',
    #         data={
    #             "email_address": "manager@test.com",
    #             "password": "testpassword",
    #             "first_name": "Test",
    #             "last_name": "User",
    #             "company": "Duck Creek",
    #             "pay_rate": 10,
    #             "is_manager": True,
    #         },
    #     )

    #     response = self.client.post(
    #         path='http://127.0.0.1:8080/account/login',
    #         data={
    #             "email_address": "manager@test.com",
    #             "password": "testpassword",
    #         },
    #     )
    #     TOKEN = json.loads(response.content)['token']

    #     response = self.client.post(
    #         path='http://127.0.0.1:8080/manager/add',
    #         headers={
    #             "Authorization": f"Bearer {TOKEN}"
    #         },
    #         data={
    #             "list_emails": ["employee2@test.com", "employee2@test.com"],
    #         }
    #     )
>>>>>>> c044538 (small changes)
