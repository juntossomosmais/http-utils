from typing import List
from unittest.mock import MagicMock

import pytest
from requests import HTTPError

from http_utils.helpers import check_for_errors
from http_utils.session import get_response_body, convert_header_to_meta_key


class TestCheckForErrors:
    @pytest.mark.parametrize(
        argnames="param_status_code_to_raise",
        argvalues=[400, 401, 403, 404, 499, 500, 501, 599],
    )
    def test_check_for_errors_must_raise_on_status_greater_than_or_equal_to_400(
            self,
            param_status_code_to_raise: int,
    ):
        mocked_response = MagicMock()
        mocked_response.status_code = param_status_code_to_raise
        with pytest.raises(HTTPError):
            check_for_errors(response=mocked_response)

    @pytest.mark.parametrize(
        argnames="param_response_status_code, param_status_codes_to_not_raise",
        argvalues=[(400, [400]), (401, [401]), (403, [403, 500])],
    )
    def test_check_for_errors_must_raise_on_status_greater_than_or_equal_to_400(
            self,
            param_response_status_code: int,
            param_status_codes_to_not_raise: List[int],
    ):
        mocked_response = MagicMock()
        mocked_response.status_code = param_response_status_code
        assert (
                check_for_errors(
                    response=mocked_response,
                    allowed_http_error_status_list=param_status_codes_to_not_raise,
                )
                is None
        )


class TestGetResponseBody:
    def test_must_parse_response_as_json(self):
        assert get_response_body(response=MagicMock())


class TestConvertHeaderToMetaKey:
    def test_must_return_none_when_no_header_is_provided(self):
        assert convert_header_to_meta_key(header=None) is None

    def test_must_parse_header(self):
        assert convert_header_to_meta_key(header="some-header") == "HTTP_SOME_HEADER"