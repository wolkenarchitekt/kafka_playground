import datetime
import logging
from typing import Optional

import psycopg2
import psycopg2.extras
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError

KAFKA_BROKER = "kafka:9092"
KAFKA_GROUP_ID = "mygroup"
KAFKA_TOPIC = "website_monitor"
KAFKA_SCHEMA_REGISTRY_URL = "http://kafka:8081"

POSTGRES_HOST = "postgres"
POSTGRES_DB = "website_status"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_PORT = 5432

logger = logging.getLogger(__name__)


def db_query():
    conn = psycopg2.connect(
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        cursor_factory=psycopg2.extras.DictCursor,
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM website_status;")
    rows = cursor.fetchall()
    return rows


def db_insert(
    status_code: int, timestamp: datetime.datetime, matches_regex: Optional[bool]
):
    conn = psycopg2.connect(
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
    )
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO website_status(status_code, timestamp, matches_regex) "
        "VALUES(%s, %s, %s)",
        (status_code, timestamp, matches_regex),
    )
    conn.commit()


def consume():
    from ipdb import set_trace; set_trace()
    c = AvroConsumer(
        {
            "bootstrap.servers": KAFKA_BROKER,
            "group.id": "groupid",
            "schema.registry.url": KAFKA_SCHEMA_REGISTRY_URL,
        }
    )

    c.subscribe([KAFKA_TOPIC])

    while True:
        try:
            msg = c.poll(1)

        except SerializerError as e:
            print("Message deserialization failed for {}: {}".format(msg, e))
            break

        if msg is None:
            continue

        if msg.error():
            print("AvroConsumer error: {}".format(msg.error()))
            continue

        timestamp = datetime.datetime.fromisoformat(msg.key()["timestamp"])
        status_code = msg.value()["status_code"]
        matches_regex = msg.value()["matches_regex"]
        db_insert(
            status_code=status_code, timestamp=timestamp, matches_regex=matches_regex
        )

    c.close()


if __name__ == "__main__":
    consume()
