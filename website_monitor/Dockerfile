FROM python:3.7-slim

RUN apt-get update \
    && apt-get install -y iputils-ping \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY website_monitor/requirements.txt .

RUN pip install -r requirements.txt

COPY website_monitor .
RUN python setup.py install
