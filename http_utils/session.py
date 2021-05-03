"""
Main HTTP session module
"""
import functools

from contextlib import contextmanager
from typing import Any
from typing import FrozenSet
from typing import Generator
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from http_utils.hooks import check_for_errors
from http_utils.hooks import log_response
from http_utils.settings import HTTP_BACKOFF_FACTOR
from http_utils.settings import HTTP_RETRIES
from http_utils.settings import HTTP_STATUS_FORCELIST
from http_utils.settings import HTTP_TIMEOUT


@contextmanager
def request_session(
    allowed_http_error_status_list: Optional[List[int]] = None,
    total: int = HTTP_RETRIES,
    backoff_factor: float = HTTP_BACKOFF_FACTOR,
    status_forcelist: Optional[Tuple] = HTTP_STATUS_FORCELIST,
    allowed_methods: Union[FrozenSet] = Retry.DEFAULT_ALLOWED_METHODS,
    **kwargs: Any,
) -> Generator[Session, None, None]:
    """
    Generate a requests session that allows retries and raises HTTP errors (status code >= 400).
    Uses the same arguments as the class Retry from urllib3
    """
    # creates new requests session
    session = Session()
    # Adds the [allowed_http_error_status_list] to the check for errors hook.
    functools.partial(
        check_for_errors,
        allowed_http_error_status_list=allowed_http_error_status_list,
    )
    session.request = functools.partial(session.request, timeout=HTTP_TIMEOUT)
    session.hooks.update(response=[log_response, check_for_errors])

    adapter = HTTPAdapter(
        max_retries=Retry(
            total=total,
            backoff_factor=backoff_factor,
            method_whitelist=allowed_methods,
            status_forcelist=status_forcelist,
            **kwargs,
        )
    )

    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        yield session
    finally:
        session.close()
