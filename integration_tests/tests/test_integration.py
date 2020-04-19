import datetime

import pytest

import psycopg2
import responses
from http_check_consumer.config import PostgresConfig
from http_check_consumer.consumer_to_db import ConsumerToDB
from http_check_producer.http_check import http_check
from http_check_producer.producer import HttpCheckProducer

WEBSITE_URL = "http://website"


@pytest.fixture
@responses.activate
def http_check_result(freezer):
    responses.add(
        responses.GET, WEBSITE_URL, status=200, content_type="text/html",
    )
    result = http_check("http://website", None)
    return result


@pytest.fixture
def http_check_kafka_produce(http_check_result, kafka_producer_config):
    # Push http check result to Kafka
    HttpCheckProducer(config=kafka_producer_config).produce(http_check_result)


@pytest.fixture
def http_check_consume_to_db(
    http_check_kafka_produce, kafka_consumer_config, postgres_config
):
    # Consume http check result from Kafka and save to DB
    consumer = ConsumerToDB(
        kafka_config=kafka_consumer_config, postgres_config=postgres_config
    )
    consumer.consume_next_message()


def query_postgres(postgres_config: PostgresConfig):
    conn = psycopg2.connect(
        database=postgres_config.database,
        user=postgres_config.user,
        password=postgres_config.password,
        host=postgres_config.host,
        port=postgres_config.port,
        cursor_factory=psycopg2.extras.DictCursor,
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM http_check")
    return cursor.fetchall()


def test_http_check(http_check_result):
    assert http_check_result.status_code == 200
    assert http_check_result.match_regex is None
    assert http_check_result.timestamp == datetime.datetime.now(
        tz=datetime.timezone.utc
    )


def test_consumed_message_is_inserted_to_db(http_check_consume_to_db, postgres_config):
    result = query_postgres(postgres_config)
    assert len(result)
