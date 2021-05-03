from unittest.mock import MagicMock

from http_utils.helpers import convert_header_to_meta_key, get_response_body


class TestGetResponseBody:
    def test_must_parse_response_as_json(self):
        assert get_response_body(response=MagicMock())


class TestConvertHeaderToMetaKey:
    def test_must_return_none_when_no_header_is_provided(self):
        assert convert_header_to_meta_key(header=None) is None

    def test_must_parse_header(self):
        assert convert_header_to_meta_key(header="some-header") == "HTTP_SOME_HEADER"
