"""
HTTP utils module
"""
import functools
from contextlib import contextmanager
from typing import Any, Dict, Generator, List, Optional

from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from http_utils.helpers import check_for_errors, log_response


@contextmanager
def request(
    total: int = 3,
    backoff_factor: float = 0.1,
    allowed_http_error_status_list: Optional[List[int]] = None,
    **kwargs: Any,
) -> Generator[Session, None, None]:
    """
    Generate a requests session that allows retries and raises HTTP errors (status code >= 400).
    Uses the same arguments as the class Retry from urllib3
    """
    functools.partial(
        check_for_errors,
        allowed_http_error_status_list=(
            allowed_http_error_status_list
            if allowed_http_error_status_list
            else None
        ),
    )
    session = Session()
    session.hooks.update(response=[log_response, check_for_errors])

    adapter = HTTPAdapter(max_retries=Retry(total=total, backoff_factor=backoff_factor, **kwargs))

    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.request = functools.partial(session.request, timeout=float(30))  # Seconds
    try:
        yield session
    finally:
        session.close()


def get_response_body(response: Response) -> Dict:
    """
    Deserialize the response.
    """
    try:
        response_body = response.json()
    except ValueError:
        response_body = response.text
    return response_body


def convert_header_to_meta_key(header: Optional[str]) -> Optional[str]:
    """
    Django Http Request has a dictionary called META with the request headers.
    But it replace the header name following the rules:
      - all characters to uppercase
      - replacing any hyphens with underscores
      - adding an HTTP_ prefix to the name.
    So, for example, a header called X-Bender would be mapped to the META key HTTP_X_BENDER.
    """
    if header is None:
        return None

    return f"HTTP_{header.replace('-', '_')}".upper()
