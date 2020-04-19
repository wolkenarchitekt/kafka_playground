import datetime
import logging
import os

from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")
KAFKA_SCHEMA_REGISTRY_URL = os.environ.get(
    "KAFKA_SCHEMA_REGISTRY_URL", "http://kafka:8081"
)
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "website_monitor")

AVRO_KEY_SCHEMA = "/avro_schema/check_result_key.avsc"
AVRO_VALUE_SCHEMA = "/avro_schema/check_result_value.avsc"

logger = logging.getLogger(__name__)


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        logger.error("Message delivery failed: {}", err)
    else:
        logger.info("Message delivered to {} [{}]".format(msg.topic(), msg.partition()))


def produce(
    timestamp: datetime.datetime,
    status_code: int,
    matches_regex: bool,
    response_time_seconds: float,
):
    value_schema = avro.load(AVRO_VALUE_SCHEMA)
    key_schema = avro.load(AVRO_KEY_SCHEMA)

    p = AvroProducer(
        {
            "bootstrap.servers": KAFKA_BROKER,
            "on_delivery": delivery_report,
            "schema.registry.url": KAFKA_SCHEMA_REGISTRY_URL,
        },
        default_key_schema=key_schema,
        default_value_schema=value_schema,
    )
    key = {"timestamp": timestamp.isoformat()}
    value = {
        "status_code": status_code,
        "matches_regex": matches_regex,
        "response_time_seconds": response_time_seconds,
    }
    p.produce(topic=KAFKA_TOPIC, value=value, key=key)
    p.flush()
