import logging

from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

from http_check_producer.config import KafkaConfig
from http_check_producer.http_check import HttpCheckResult

logger = logging.getLogger(__name__)


class HttpCheckProducer:
    def __init__(self, config: KafkaConfig):
        self.config = config

    @staticmethod
    def delivery_report(err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            logger.error("Message delivery failed: {}", err)
        else:
            logger.info(
                "Message delivered to {} [{}]".format(msg.topic(), msg.partition())
            )

    def produce(
        self, http_check_result: HttpCheckResult,
    ):
        key_schema = avro.load(self.config.avro_key_schema)
        value_schema = avro.load(self.config.avro_value_schema)

        p = AvroProducer(
            {
                "bootstrap.servers": self.config.broker,
                "on_delivery": self.delivery_report,
                "schema.registry.url": self.config.schema_registry_url,
            },
            default_key_schema=key_schema,
            default_value_schema=value_schema,
        )
        key = {"timestamp": http_check_result.timestamp.isoformat()}
        value = {
            "status_code": http_check_result.status_code,
            "matches_regex": http_check_result.match_regex,
            "response_time_seconds": http_check_result.response_time_seconds,
        }
        logger.debug(f"Produced message: {key} {value}")
        p.produce(topic=self.config.topic, value=value, key=key)
        p.flush()
