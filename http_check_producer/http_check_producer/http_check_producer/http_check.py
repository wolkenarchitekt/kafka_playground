import datetime
import logging
import re
from dataclasses import dataclass
from typing import Optional, Pattern

import requests

logger = logging.getLogger(__name__)


@dataclass
class HttpCheckResult:
    status_code: int
    timestamp: datetime.datetime
    match_regex: Optional[bool]
    response_time_seconds: float


def http_check(
    url: str, regex_pattern: Optional[Pattern] = None
) -> HttpCheckResult:
    response = requests.get(url)
    timestamp = datetime.datetime.now(tz=datetime.timezone.utc)
    check_result = HttpCheckResult(
        status_code=response.status_code,
        timestamp=timestamp,
        match_regex=None,
        response_time_seconds=response.elapsed.total_seconds(),
    )
    if regex_pattern:
        content = response.content.decode()
        regex_matches = len(re.findall(regex_pattern, content)) > 0
        check_result.match_regex = regex_matches
    return check_result
