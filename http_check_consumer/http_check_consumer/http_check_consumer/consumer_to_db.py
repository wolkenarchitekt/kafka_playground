import logging

from http_check_consumer.consumer import HttpCheckConsumer, KafkaConfig
from http_check_consumer.db import HttpCheckDB, PostgresConfig
from http_check_consumer.message_types import HttpCheckResult

logger = logging.getLogger(__name__)


class ConsumerToDB:
    """Consume HTTP Check messages from Kafka and write to DB"""

    def __init__(self, kafka_config: KafkaConfig, postgres_config: PostgresConfig):
        self._db = HttpCheckDB(config=postgres_config)
        self._consumer = HttpCheckConsumer(config=kafka_config)
        self._consume_gen = self._consumer.consume()

    def _process_check_result(self, check_result: HttpCheckResult):
        """Write check result to DB, commit Kafka consumer when successful"""
        self._db.insert_check_result(check_result)
        self._consumer.commit()

    def consume_messages(self):
        """Consume messages forever and write each message to DB"""
        for check_result in self._consume_gen:
            self._process_check_result(check_result)

    def consume_next_message(self):
        """Consume next Kafka message and write to DB"""
        message = next(self._consume_gen)
        self._process_check_result(message)
