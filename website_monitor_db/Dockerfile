FROM python:3.7-slim

RUN apt-get update \
    && apt-get install -y iputils-ping libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY website_monitor_db/requirements.txt .

RUN pip install -r requirements.txt

COPY website_monitor_db .
RUN python setup.py install
