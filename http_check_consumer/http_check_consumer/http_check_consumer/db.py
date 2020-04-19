import logging

import psycopg2
import psycopg2.extras
from http_check_consumer.config import PostgresConfig
from http_check_consumer.message_types import HttpCheckResult

logger = logging.getLogger(__name__)


class HttpCheckDB:
    def __init__(self, config: PostgresConfig):
        self.config = config
        self.conn = psycopg2.connect(
            database=self.config.database,
            user=self.config.user,
            password=self.config.password,
            host=self.config.host,
            port=self.config.port,
        )
        self.cursor = self.conn.cursor()

    def insert_check_result(
        self, result: HttpCheckResult,
    ):
        """Insert check result to database"""
        self.cursor.execute(
            "INSERT INTO http_check("
            "status_code, timestamp, matches_regex, response_time_seconds) "
            "VALUES(%s, %s, %s, %s)",
            (
                result.status_code,
                result.timestamp,
                result.matches_regex,
                result.response_time_seconds,
            ),
        )
        self.conn.commit()
