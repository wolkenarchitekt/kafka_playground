import os
from dataclasses import dataclass


@dataclass
class KafkaConfig:
    broker: str
    group_id: str
    topic: str
    schema_registry_url: str
    avro_key_schema: str
    avro_value_schema: str


def get_config_from_env():
    return KafkaConfig(
        broker=os.environ["KAFKA_BROKER"],
        group_id=os.environ["KAFKA_GROUP_ID"],
        topic=os.environ["KAFKA_TOPIC"],
        schema_registry_url=os.environ["KAFKA_SCHEMA_REGISTRY_URL"],
        avro_key_schema=os.environ["KAFKA_AVRO_KEY_SCHEMA"],
        avro_value_schema=os.environ["KAFKA_AVRO_VALUE_SCHEMA"],
    )
