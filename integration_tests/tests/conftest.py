import pytest

from http_check_consumer.config import KafkaConfig as ConsumerKafkaConfig
from http_check_consumer.config import PostgresConfig
from http_check_producer.config import KafkaConfig as ProducerKafkaConfig

KAFKA_BROKER = "kafka:9092"
KAFKA_GROUP_ID = "mygroup"
KAFKA_TOPIC = "http_check_producer"
KAFKA_SCHEMA_REGISTRY_URL = "http://kafka:8081"
KAFKA_AVRO_KEY_SCHEMA = "/avro_schema/check_result_key.avsc"
KAFKA_AVRO_VALUE_SCHEMA = "/avro_schema/check_result_value.avsc"

POSTGRES_HOST = "postgres"
POSTGRES_DB = "http_check"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_PORT = 5432


@pytest.fixture
def kafka_producer_config():
    return ProducerKafkaConfig(
        broker="kafka:9092",
        group_id="mygroup",
        topic="http_check_producer",
        schema_registry_url="http://kafka:8081",
        avro_key_schema="/avro_schema/check_result_key.avsc",
        avro_value_schema="/avro_schema/check_result_value.avsc",
    )


@pytest.fixture
def kafka_consumer_config():
    return ConsumerKafkaConfig(
        broker="kafka:9092",
        group_id="mygroup",
        topic="http_check_producer",
        schema_registry_url="http://kafka:8081",
    )


@pytest.fixture
def postgres_config():
    return PostgresConfig(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        port=POSTGRES_PORT,
    )
