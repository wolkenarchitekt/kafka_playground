FROM python:3.7-slim

RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY wait-for-it.sh /wait-for-it.sh

WORKDIR /app

COPY http_check_consumer/requirements.txt .

RUN pip install -r requirements.txt

COPY http_check_consumer .
RUN python setup.py install
