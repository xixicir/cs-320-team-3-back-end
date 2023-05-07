#!/bin/bash

# Django setup
python manage.py makemigrations auth_user time_log
python manage.py migrate

# Start gunicorn service
gunicorn -c scripts/service_cfg.py
