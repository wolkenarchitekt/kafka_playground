import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class HttpCheckResult:
    status_code: int
    matches_regex: Optional[bool]
    timestamp: datetime.datetime
    response_time_seconds: float
