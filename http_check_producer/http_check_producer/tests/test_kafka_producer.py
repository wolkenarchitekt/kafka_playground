import datetime
from unittest.mock import patch

from http_check_producer.http_check import HttpCheckResult
from http_check_producer.producer import HttpCheckProducer, KafkaConfig


@patch("http_check_producer.producer.AvroProducer.produce")
def test_kafka_producer(mock_produce):
    kafka_config = KafkaConfig(
        broker="fake",
        group_id="fake",
        topic="fake",
        schema_registry_url="http://fake_url",
        avro_key_schema="/avro_schema/check_result_key.avsc",
        avro_value_schema="/avro_schema/check_result_value.avsc",
    )
    producer = HttpCheckProducer(config=kafka_config)
    mock_produce.return_value = None
    check_result = HttpCheckResult(
        status_code=200,
        match_regex=False,
        response_time_seconds=1.0,
        timestamp=datetime.datetime.now(),
    )
    producer.produce(http_check_result=check_result)
    mock_produce.assert_called()
