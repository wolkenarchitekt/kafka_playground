import datetime
from unittest.mock import patch
from website_monitor.kafka_producer import produce


@patch("website_monitor.kafka_producer.AvroProducer.produce")
def test_kafka_producer(mock_produce):
    mock_produce.return_value = None
    produce(datetime.datetime.now(), 200, False, 1.0)
    mock_produce.assert_called()
