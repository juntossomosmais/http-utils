from typing import List

import httpretty as httpretty
import pytest

from requests import HTTPError

from http_utils.session import request_session


class TestAllowedHttpErrorStatusList:
    fake_uri = "https://www.baNanNa.com.br"

    @httpretty.activate
    @pytest.mark.parametrize(argnames="param_status_code", argvalues=[400, 401, 403, 404, 499, 500, 503, 599])
    def test_session_must_raise_on_error(self, param_status_code: int):
        httpretty.register_uri(
            httpretty.GET,
            uri=self.fake_uri,
            status=param_status_code,
        )
        with pytest.raises(HTTPError):
            with request_session() as request:
                request.get(url=self.fake_uri)

    @httpretty.activate
    @pytest.mark.parametrize(
        argnames="param_status_code, param_status_to_not_raise",
        argvalues=[(400, [400]), (401, [401, 500])],
    )
    def test_session_must_not_raise_when_returned_status_code_is_marked_to_not_raise(
        self, param_status_code: int, param_status_to_not_raise: List[int]
    ):
        httpretty.register_uri(
            httpretty.GET,
            uri=self.fake_uri,
            status=param_status_code,
        )
        with pytest.raises(HTTPError):
            with request_session(allowed_http_error_status_list=param_status_to_not_raise) as request:
                request.get(url=self.fake_uri)
