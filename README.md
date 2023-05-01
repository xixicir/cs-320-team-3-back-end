# Time Punch

Brief description...

## Installation

### Local

```bash
# Python setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start postgres
sudo systemctl start postgresql
```

### Docker

```bash
# run the docker compose (you need to install docker first)
# If you haven't build the docker, (if you already build, no need to add --build )
docker compose up --build
```

## Usage

```bash
# Steps to create a new app
python manage.py startapp auth_user

# After making edits to models.py
python manage.py makemigrations auth_user
python manage.py migrate

# Export env var to use postgres
export DB_TYPE=postgres # or sqlite
export DB_HOST=localhost # or db

# Start wsgi server for development
python manage.py runserver 0.0.0.0:8080

# Or start gunicorn server
gunicorn -c service_cfg.py
```

### Testing

#### cURL calls

```bash
curl -X 'POST' \
          'http://127.0.0.1:8080/account/create' \
          -H 'accept: application/json' \
          -H 'Content-Type: application/json' \
          -d '{
          "email_address": "john.doe@gmail.com",
          "password": "passwordThis123",
          "pay_rate": 45,
          "company": "google",
          "first_name": "John",
          "last_name": "Doe"
}'

curl -X 'POST' \
          'http://127.0.0.1:8080/account/create' \
          -H 'accept: application/json' \
          -H 'Content-Type: application/json' \
          -d '{
          "email_address": "jason.boe@gmail.com",
          "password": "passwordThis123",
          "pay_rate": 35,
          "company": "apple",
          "first_name": "Jason",
          "last_name": "Boe"
}'

export TOKEN=$(curl -X 'POST' \
          'http://127.0.0.1:8080/account/login' \
          -H 'accept: application/json' \
          -H 'Content-Type: application/json' \
          -d '{
          "email_address": "john.doe@gmail.com",
          "password": "passwordThis123"
        }' | jq -r .token)

# After running simulate_workflow/generate_users.py
export TOKEN=$(curl -X 'POST' \
          'http://127.0.0.1:8080/account/login' \
          -H 'accept: application/json' \
          -H 'Content-Type: application/json' \
          -d '{
          "email_address": "Betty_Burke@gizmogram.com",
          "password": "burkebe"
        }' | jq -r .token)

curl -H "Authorization: Bearer $TOKEN" \
                "http://127.0.0.1:8080/account/verify"

curl -H "Authorization: Bearer $TOKEN" \
                "http://127.0.0.1:8080/account/get"

curl -X GET "http://127.0.0.1:8080/account/view" \
                -H "Authorization: Bearer $TOKEN" \
                -H 'Content-Type: application/json'\
                -d '{"email_address": "john.doe@gmail.com"}'

curl -X 'POST' \
          'http://127.0.0.1:8080/manager/add' \
          -H "Authorization: Bearer $TOKEN" \
          -H 'accept: application/json' \
          -H 'Content-Type: application/json' \
          -d '{"list_emails": ["jason.boe@gmail.com"]}'

curl -X 'POST' \
          'http://127.0.0.1:8080/manager/remove' \
          -H "Authorization: Bearer $TOKEN" \
          -H 'accept: application/json' \
          -H 'Content-Type: application/json' \
          -d '{"list_emails": ["jason.boe@gmail.com"]}'

curl -X GET "http://127.0.0.1:8080/manager/get" \
                -H "Authorization: Bearer $TOKEN"

curl -X 'POST' \
          'http://127.0.0.1:8080/time/log' \
          -H "Authorization: Bearer $TOKEN" \
          -H 'accept: application/json' \
          -H 'Content-Type: application/json' \
          -d '{
            "start": "2022-08-28T04:35:35.455Z",
            "end": "2022-08-28T09:36:35.455Z"
          }'

curl -X GET "http://127.0.0.1:8080/time/get" \
                -H "Authorization: Bearer $TOKEN"

curl -X GET "http://127.0.0.1:8080/time/employees" \
                -H "Authorization: Bearer $TOKEN"

curl -X GET "http://127.0.0.1:8080/employee/pay" \
                -H "Authorization: Bearer $TOKEN"

curl -X 'POST' \
          'http://127.0.0.1:8080/employee/pay' \
          -H "Authorization: Bearer $TOKEN" \
          -H 'accept: application/json' \
          -H 'Content-Type: application/json' \
          -d '{"pay_rate": 23.78}'
```

#### JSON simulation

```bash
# Limit of 100 (providing no limit runs it on all datapoints)
python simulate_workflow/generate_users.py 100
```

#### Unit testing

```bash
python manage.py test
```
