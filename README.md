# Time Punch

Brief description...

## Installation

### Local
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Docker
```bash
TODO
```

## Usage
```bash
# Steps to create a new app
python manage.py startapp auth_user

# After making edits to models.py
python manage.py makemigrations auth_user
python manage.py migrate

# Start server
python manage.py runserver 0.0.0.0:8080
```


### Testing

Example cURL calls
```bash
curl -X POST  "http://127.0.0.1:8080/account/create" \
                          -d email_address=john.doe@gmail.com \
                           -d password=passwordThis123 \
                           -d company=google \
                           -d first_name=John \
                           -d last_name=Doe

curl -X POST  "http://127.0.0.1:8080/account/login" \
                          -d email_address=john.doe@gmail.com \
                           -d password=passwordThis1234

curl -H "Authorization: Bearer TOKEN_HERE" \
                "http://127.0.0.1:8080/account/verify"
```
