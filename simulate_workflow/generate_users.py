import sys

from parse_json import get_all_dicts
from random import randint
from tqdm import tqdm
import json
import requests
from datetime import datetime, timedelta

HOST_IP = "http://127.0.0.1:8080"

headers = {"Content-type": "application/json", "Accept": "application/json"}


def get_random_rate():
    return randint(20, 150)


def get_hour_diff(diff):
    days, seconds = diff.days, diff.seconds
    return days * 24 + seconds // 3600


def strp_delta(s):
    hr, min, sec = map(float, s.split(":"))
    return timedelta(hours=hr, minutes=min, seconds=sec)


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

    requests.post(
        f"{HOST_IP}/manager/add", headers=headers, data=json.dumps(data)
    )


def add_time_log(usr_token, start_dt, end_dt):
    headers["Authorization"] = f"Bearer {usr_token}"
    data = {"start": start_dt, "end": end_dt}
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
            dt_format = "%Y-%m-%dT%H:%M:%S.%fZ"
            dt_start = dt_end = ""

            if "date" in t_entry:
                dt_start = datetime.strptime(t_entry["date"], "%Y-%m-%d")

            if "hoursWorked" in t_entry:
                dt_end = dt_start + timedelta(hours=t_entry["hoursWorked"])

            if "clockedIn" in t_entry:
                day = dt_start
                dt_start = day + strp_delta(t_entry["clockedIn"])
                dt_end = day + strp_delta(t_entry["clockedIn"])

            if "clockedInEpochMillisecond" in t_entry:
                dt_start = datetime.fromtimestamp(
                    int(t_entry["clockedInEpochMillisecond"]) / 1000.0
                )
                dt_end = datetime.fromtimestamp(
                    int(t_entry["clockedOutEpochMillisecond"]) / 1000.0
                )

            parsed_start, parsed_end = map(
                lambda d: d.strftime(dt_format), (dt_start, dt_end)
            )
            add_time_log(list_tokens[i], parsed_start, parsed_end)


add_all_info(limit=int(sys.argv[1]) if len(sys.argv) > 1 else 10**5)
