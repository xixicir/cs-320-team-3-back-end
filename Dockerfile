FROM python:3.11-slim-buster

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt update -y 
RUN apt-get install libpq-dev python3-dev -y

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 8080

RUN python manage.py makemigrations auth_user time_log
RUN python manage.py migrate
