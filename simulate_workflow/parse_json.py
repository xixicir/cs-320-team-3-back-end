from glob import glob
import json
import os

BASE_DIR = "data-export"
assert os.path.isdir(BASE_DIR)


def get_employee_files():
    return glob(f"{BASE_DIR}/*-employees.json")


def get_time_files():
    return glob(f"{BASE_DIR}/*-entries.json")


def get_dicts(list_files, limit=100):
    lst_dts = list()
    for idx, fname in enumerate(sorted(list_files)):
        with open(fname, "r") as f:
            lst_this = json.load(f)

            for item in lst_this:
                item["companyId"] = idx

            lst_dts.extend(lst_this[:limit])
    return lst_dts


def get_all_dicts(limit):
    return get_dicts(get_employee_files(), limit), get_dicts(get_time_files(), limit)
