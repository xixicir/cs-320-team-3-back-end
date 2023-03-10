from glob import glob
import json
import os

BASE_DIR = "data-export"
assert os.path.isdir(BASE_DIR)


def get_employee_files():
    return glob(f"{BASE_DIR}/*-employees.json")


def get_time_files():
    return glob(f"{BASE_DIR}/*-entries.json")


def get_dicts(list_files):
    lst_dts = list()
    for fname in list_files:
        with open(fname, "r") as f:
            lst_this = json.load(f)
            lst_dts.extend(lst_this)
    return lst_dts


# print(get_dicts(get_employee_files())[:2])
# print(get_dicts(get_time_files())[:2])

