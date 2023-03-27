#!/bin/bash

python manage.py makemigrations auth_user time_log
python manage.py migrate
# python manage.py runserver 0.0.0.0:8080
gunicorn -c service_cfg.py
