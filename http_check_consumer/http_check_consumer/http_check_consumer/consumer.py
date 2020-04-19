import datetime
import logging
from typing import Generator

from confluent_kafka.avro import AvroConsumer, SerializerError

from http_check_consumer.config import KafkaConfig
from http_check_consumer.message_types import HttpCheckResult

KAFKA_BROKER = "kafka:9092"
KAFKA_GROUP_ID = "mygroup"
KAFKA_TOPIC = "http_check_producer"
KAFKA_SCHEMA_REGISTRY_URL = "http://kafka:8081"

logger = logging.getLogger(__name__)


class HttpCheckSerializerError(Exception):
    pass


class HttpCheckConsumerError(Exception):
    pass


class HttpCheckConsumer:
    """Consume Kafka messages"""

    def __init__(self, config: KafkaConfig):
        self.config = config
        self.consumer = AvroConsumer(
            {
                "bootstrap.servers": KAFKA_BROKER,
                "group.id": "groupid",
                "schema.registry.url": KAFKA_SCHEMA_REGISTRY_URL,
                "auto.offset.reset": "smallest",
                "enable.auto.commit": False,
            }
        )
        self.consumer.subscribe([KAFKA_TOPIC])

    @staticmethod
    def _process_message(message) -> HttpCheckResult:
        key = message.key()
        value = message.value()
        timestamp = datetime.datetime.fromisoformat(key["timestamp"])
        status_code = value["status_code"]
        matches_regex = value["matches_regex"]
        response_time_seconds = value["response_time_seconds"]
        return HttpCheckResult(
            status_code=status_code,
            timestamp=timestamp,
            matches_regex=matches_regex,
            response_time_seconds=response_time_seconds,
        )

    def consume(self) -> Generator[HttpCheckResult, None, None]:
        while True:
            try:
                msg = self.consumer.poll(1)
            except SerializerError as error:
                raise HttpCheckSerializerError(
                    f"Message deserialization failed: {error}"
                )

            if msg is None:
                continue

            if msg.error():
                raise HttpCheckConsumerError(
                    "AvroConsumer error: {}".format(msg.error())
                )

            logger.debug(f"Offset: {msg.offset()}")
            yield self._process_message(msg)

    def commit(self):
        self.consumer.commit()
