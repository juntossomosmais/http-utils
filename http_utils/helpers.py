"""
Helper module for the main HTTP utils
"""
import logging
from typing import Any, List, Optional

from requests import Response


def log_response(response: Response, *args: Any, **kwargs: Any) -> None:
    """
    Logs the obtained response.
    """
    logging.debug(
        "Request to %s returned status code %d", response.url, response.status_code
    )


def check_for_errors(
    response: Response,
    allowed_http_error_status_list: Optional[List[int]] = None,
    *args: Any,
    **kwargs: Any,
) -> None:
    """
    Raises a [HTTPError] based on response status that are greater than or equal 400.

    :param: 'allowed_http_error_status' is a list of status codes that can be provided
    to not raise a [HTTPError]
    """
    allowed_http_error_status_list = (
        allowed_http_error_status_list
        if isinstance(allowed_http_error_status_list, list)
        else []
    )
    if all(status >= 400 for status in allowed_http_error_status_list):
        response.raise_for_status()
