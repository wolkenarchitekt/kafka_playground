import datetime
from unittest.mock import patch

from http_check_consumer.consumer import HttpCheckConsumer, KafkaConfig
from http_check_consumer.message_types import HttpCheckResult


@patch("http_check_consumer.consumer.AvroConsumer.poll")
@patch("http_check_consumer.consumer.AvroConsumer.subscribe")
def test_consume_kafka_message_succeeds(mock_subscribe, mock_poll, freezer):
    class MockPoll:
        def value(self):
            return {
                "status_code": 200,
                "matches_regex": None,
                "response_time_seconds": 1.02,
            }

        def key(self):
            return {"timestamp": datetime.datetime.now().isoformat()}

        def error(self):
            return None

        def offset(self):
            return 0

    kafka_config = KafkaConfig(
        broker="fake", group_id="fake", topic="fake", schema_registry_url="fake"
    )

    mock_poll.return_value = MockPoll()
    consumer = HttpCheckConsumer(config=kafka_config)
    result = next(consumer.consume())
    assert result == HttpCheckResult(
        status_code=200,
        timestamp=datetime.datetime.now(),
        matches_regex=None,
        response_time_seconds=1.02,
    )
    mock_poll.assert_called()
    mock_subscribe.assert_called()
