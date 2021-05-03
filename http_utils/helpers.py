"""
Helpers module for handling HTTP Response and Header objects.
"""
from typing import Optional, Dict

from requests import Response


def convert_header_to_meta_key(header: Optional[str]) -> Optional[str]:
    """
    Django Http Request has a dictionary called META with the request_session headers.
    But it replace the header name following the rules:
      - all characters to uppercase
      - replacing any hyphens with underscores
      - adding an HTTP_ prefix to the name.
    So, for example, a header called X-Bender would be mapped to the META key HTTP_X_BENDER.
    """
    if header is None:
        return None

    return f"HTTP_{header.replace('-', '_')}".upper()


def get_response_body(response: Response) -> Dict:
    """
    Deserialize the response returning a deserialized json dict or a text.

    :param response:
        Response object from `requests` module.
    """
    try:
        response_body = response.json()
    except ValueError:
        response_body = response.text
    return response_body
