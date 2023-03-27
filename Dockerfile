FROM python:3.11-slim-buster

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY requirements.txt .
RUN apt update -y 
RUN apt-get install libpq-dev -y
RUN pip3 install -r requirements.txt

COPY . .
# RUN chmod +x docker-entrypoint.sh
EXPOSE 8080
# ENTRYPOINT [ "docker-entrypoint.sh" ]
# RUN python manage.py startapp auth_user
RUN python manage.py makemigrations auth_user
RUN python manage.py migrate
