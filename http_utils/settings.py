import os

from http import HTTPStatus
from typing import Iterable

HTTP_RETRIES = int(os.getenv("HTTP_RETRIES", 3))
HTTP_BACKOFF_FACTOR = float(os.getenv("HTTP_BACKOFF_FACTOR", 0.1))
HTTP_STATUS_FORCELIST: Iterable[int | str | HTTPStatus] = os.getenv("HTTP_STATUS_FORCELIST", []) or []
HTTP_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", 30))
