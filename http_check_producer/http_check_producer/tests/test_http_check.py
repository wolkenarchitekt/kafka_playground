import datetime
import re

import pytest

import responses
from http_check_producer.http_check import http_check

WEBSITE_URL = "http://website"


@pytest.fixture
def success_response():
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            WEBSITE_URL,
            body="Hello",
            status=200,
            content_type="text/html",
        )
        yield rsps


def test_website_check_with_200_response(freezer, success_response):
    result = http_check(WEBSITE_URL)
    assert result.status_code == 200
    assert result.match_regex is None
    assert result.timestamp == datetime.datetime.now(tz=datetime.timezone.utc)


@responses.activate
def test_website_check_with_404_response():
    responses.add(
        responses.GET, WEBSITE_URL, status=404, content_type="text/html",
    )
    result = http_check(WEBSITE_URL)
    assert result.status_code == 404


def test_website_check_regex_matches(success_response):
    result = http_check(WEBSITE_URL, regex_pattern=re.compile("Hello"))
    assert result.match_regex


def test_website_check_regex_doesnt_match(success_response):
    result = http_check(WEBSITE_URL, regex_pattern=re.compile("Foobar"))
    assert not result.match_regex
