from locust import HttpUser, task, between
from faker import Faker
from datetime import timedelta

fake = Faker()


class DjangoUser(HttpUser):
    wait_time = between(1, 2.5)

    def on_start(self):
        self.email_address = fake.email()
        self.password = fake.password(
            length=12, special_chars=True, digits=True, upper_case=True, lower_case=True
        )
        self.pay_rate = fake.random.uniform(20, 50)
        self.company = fake.company()
        self.first_name = fake.first_name()
        self.last_name = fake.last_name()

        self.create_account()
        self.verify_account()

    def create_account(self):
        payload = {
            "email_address": self.email_address,
            "password": self.password,
            "pay_rate": self.pay_rate,
            "company": self.company,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
        response = self.client.post("/account/create", json=payload)
        if response.status_code == 200:
            self.token = response.json().get("token")

    def verify_account(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/account/verify", headers=headers)

    @task
    def get_account(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/account/get", headers=headers)

    @task
    def view_account(self):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        payload = {"email_address": self.email_address}
        self.client.get("/account/view", headers=headers, json=payload)

    @task
    def get_all_managers(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/manager/all", headers=headers)

    @task
    def add_manager(self):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        payload = {"list_emails": [fake.email()]}
        self.client.post("/manager/add", headers=headers, json=payload)

    @task
    def remove_manager(self):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        payload = {"list_emails": [fake.email()]}
        self.client.post("/manager/remove", headers=headers, json=payload)

    @task
    def get_manager(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/manager/get", headers=headers)

    @task
    def log_time(self):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        dt_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        dt_start = fake.date_time_this_month()
        dt_end = dt_start + timedelta(hours=int(fake.random.uniform(1, 9)))

        payload = {
            "start": dt_start.strftime(dt_format),
            "end": dt_end.strftime(dt_format),
        }
        self.client.post("/time/log", headers=headers, json=payload)

    @task
    def get_time(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/time/get", headers=headers)

    @task
    def get_employees_time(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/time/employees", headers=headers)

    @task
    def get_employee_pay(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/employee/pay", headers=headers)

    @task
    def update_employee_pay(self):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        payload = {"pay_rate": fake.random.uniform(20, 50)}
        self.client.post("/employee/pay", headers=headers, json=payload)
