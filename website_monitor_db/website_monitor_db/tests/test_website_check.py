import datetime
from unittest.mock import patch

from website_monitor_db.website_monitor_db import consume


@patch("website_monitor_db.website_monitor_db.AvroConsumer.poll")
@patch("website_monitor_db.website_monitor_db.AvroConsumer.subscribe")
@patch("psycopg2.connect")
def test_write_result(mock_psycop2_connect, mock_subscribe, mock_poll):
    class MockPoll:
        def value(self):
            return {
                "status_code": 200,
                "matches_regex": None,
            }

        def key(self):
            return {"timestamp": datetime.datetime.now().isoformat()}

        def error(self):
            return None

    mock_poll.return_value = MockPoll()
    consume()
    mock_poll.assert_called()
