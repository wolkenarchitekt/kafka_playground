import os
from dataclasses import dataclass


@dataclass
class PostgresConfig:
    host: str
    database: str
    user: str
    password: str
    port: int = 5432


@dataclass
class KafkaConfig:
    broker: str
    group_id: str
    topic: str
    schema_registry_url: str


def get_kafka_config_from_env() -> KafkaConfig:
    return KafkaConfig(
        broker=os.environ["KAFKA_BROKER"],
        group_id=os.environ["KAFKA_GROUP_ID"],
        topic=os.environ["KAFKA_TOPIC"],
        schema_registry_url=os.environ["KAFKA_SCHEMA_REGISTRY_URL"],
    )


def get_postgres_config_from_env() -> PostgresConfig:
    return PostgresConfig(
        host=os.environ["POSTGRES_HOST"],
        database=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        port=int(os.environ["POSTGRES_PORT"]),
    )
