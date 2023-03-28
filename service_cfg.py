HOST_PORT = 8080

wsgi_app = "timepunch.wsgi:application"
loglevel = "debug"

workers = 5

bind = f"0.0.0.0:{HOST_PORT}"

# Development only
reload = False

accesslog = "gunicorn_service.log"
capture_output = True
pidfile = "gunicorn_service.pid"
