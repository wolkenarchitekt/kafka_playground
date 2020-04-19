FROM python:3.7-slim

COPY wait-for-it.sh /wait-for-it.sh
COPY avro_schema /avro_schema

WORKDIR /app

COPY http_check_producer/requirements.txt .

RUN pip install -r requirements.txt

COPY http_check_producer .
RUN python setup.py install
