FROM python:3.11-alpine

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
RUN chmod +x docker-entrypoint.sh
EXPOSE 8080
ENTRYPOINT [ "docker-entrypoint.sh" ]
