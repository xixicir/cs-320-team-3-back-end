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

# Start wsgi server for development
python manage.py runserver 0.0.0.0:8080

# Or start gunicorn server
gunicorn -c service_cfg.py
```
### Testing

Example cURL calls

```bash
curl -X POST  "http://127.0.0.1:8080/account/create" \
                          -d email_address=john.doe@gmail.com \
                          -d password=passwordThis123 \
                          -d pay_rate=45 \
                          -d company=google \
                          -d first_name=John \
                          -d last_name=Doe

curl -X POST  "http://127.0.0.1:8080/account/create" \
                          -d email_address=jason.boe@gmail.com \
                          -d password=passwordThis123 \
                          -d pay_rate=35 \
                          -d company=apple \
                          -d first_name=Jason \
                          -d last_name=Boe

export TOKEN=$(curl -X POST  "http://127.0.0.1:8080/account/login" \
                          -d email_address=john.doe@gmail.com \
                          -d password=passwordThis123 | jq -r .token)

curl -H "Authorization: Bearer $TOKEN" \
                "http://127.0.0.1:8080/account/verify"

curl -X POST "http://127.0.0.1:8080/manager/add" \
                -H "Authorization: Bearer $TOKEN" \
                -d list_emails='["jason.boe@gmail.com"]'

curl -X POST "http://127.0.0.1:8080/manager/remove" \
                -H "Authorization: Bearer $TOKEN" \
                -d list_emails='["jason.boe@gmail.com"]'

curl -X GET "http://127.0.0.1:8080/manager/get" \
                -H "Authorization: Bearer $TOKEN"

curl -X POST "http://127.0.0.1:8080/time/log" \
                -H "Authorization: Bearer $TOKEN" \
                -d num_hours=8

curl -X GET "http://127.0.0.1:8080/time/get" \
                -H "Authorization: Bearer $TOKEN"

curl -X GET "http://127.0.0.1:8080/time/employees" \
                -H "Authorization: Bearer $TOKEN"

curl -X GET "http://127.0.0.1:8080/employee/pay" \
                -H "Authorization: Bearer $TOKEN"

curl -X POST "http://127.0.0.1:8080/employee/pay" \
                -H "Authorization: Bearer $TOKEN" \
                -d pay_rate=23.78
```
