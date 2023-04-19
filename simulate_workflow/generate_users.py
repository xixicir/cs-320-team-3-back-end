import sys

from parse_json import get_all_dicts
from random import randint
from tqdm import tqdm
import json
import requests
from datetime import datetime

HOST_IP = "http://127.0.0.1:8080"

headers = {"Content-type": "application/json", "Accept": "application/json"}


def get_random_rate():
    return randint(20, 150)


def get_hour_diff(diff):
    days, seconds = diff.days, diff.seconds
    return days * 24 + seconds // 3600


def register_user(user_dt):
    data = {
        "email_address": user_dt["email"],
        "password": user_dt["password"],
        "pay_rate": get_random_rate(),
        "company": user_dt["companyName"],
        "first_name": user_dt["firstName"],
        "last_name": user_dt["lastName"],
        "is_manager": user_dt["isManager"],
        "company_ID": user_dt["companyId"],
        "position": user_dt["positionTitle"],
        "start_date": user_dt["startDate"],
        "employee_ID": user_dt["employeeId"],
    }
    requests.post(f"{HOST_IP}/account/create", data=json.dumps(data), headers=headers)


def login_user(user_dt):
    data = {
        "email_address": user_dt["email"],
        "password": user_dt["password"],
    }
    resp = requests.post(
        f"{HOST_IP}/account/login", data=json.dumps(data), headers=headers
    )
    resp.raise_for_status()
    return resp.json()["token"]


def add_employees(manager_token, list_employees):
    if not list_employees:
        return

    headers["Authorization"] = f"Bearer {manager_token}"
    data = {"list_emails": list_employees}

    resp = requests.post(
        f"{HOST_IP}/manager/add", headers=headers, data=json.dumps(data)
    )
    resp.raise_for_status()


def add_time_log(usr_token, dt_worked, hours_worked):
    headers["Authorization"] = f"Bearer {usr_token}"
    data = {"num_hours": hours_worked, "date_logged": dt_worked}
    requests.post(f"{HOST_IP}/time/log", headers=headers, data=json.dumps(data))


def add_all_info(limit):
    list_users, list_times = get_all_dicts(limit=limit)
    list_tokens = []

    for usr in tqdm(list_users, desc="Register/login users"):
        register_user(usr)
        list_tokens.append(login_user(usr))

    for i, usr in enumerate(tqdm(list_users, desc="Assigning managers")):
        employees = [
            dt["email"]
            for dt in list_users
            if dt.get("managerId", "") == usr["employeeId"]
            and dt["companyName"] == usr["companyName"]
        ]
        add_employees(list_tokens[i], employees)

    for i, usr in enumerate(tqdm(list_users, desc="Adding time logs")):
        time_entry = next(
            (
                item
                for item in list_times
                if item["employeeId"] == usr["employeeId"]
                and item["companyId"] == usr["companyId"]
            ),
            None,
        )
        if not time_entry:
            continue
        for t_entry in time_entry["timeEntries"]:
            dt_worked = ""
            hrs_worked = 0

            for k in t_entry:
                match k:
                    case "date":
                        dt_worked = t_entry["date"]
                    case "hoursWorked":
                        hrs_worked = t_entry["hoursWorked"]
                    case "clockedIn":
                        FMT = "%H:%M:%S"
                        tdelta = datetime.strptime(
                            t_entry["clockedOut"], FMT
                        ) - datetime.strptime(t_entry["clockedIn"], FMT)
                        hrs_worked += get_hour_diff(tdelta)
                    case "clockedInEpochMillisecond":
                        dt_in = datetime.fromtimestamp(
                            int(t_entry["clockedInEpochMillisecond"]) / 1000.0
                        )
                        dt_out = datetime.fromtimestamp(
                            int(t_entry["clockedOutEpochMillisecond"]) / 1000.0
                        )
                        hrs_worked = get_hour_diff(dt_out - dt_in)
                        dt_worked = dt_in.strftime("%Y-%m-%d")

            add_time_log(list_tokens[i], dt_worked, hrs_worked)


add_all_info(limit=int(sys.argv[1]) if len(sys.argv) > 1 else 10**5)
