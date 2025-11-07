from unittest.mock import MagicMock

from http_utils.helpers import convert_header_to_meta_key
from http_utils.helpers import get_response_body


class TestGetResponseBody:
    def test_must_parse_response_as_json(self):
        assert get_response_body(response=MagicMock())

    def test_must_parse_response_as_text_when_json_fails(self):
        mocked_response = MagicMock()
        mocked_response.json.side_effect = ValueError
        mocked_response.text = "some text response"
        assert get_response_body(response=mocked_response) == "some text response"


class TestConvertHeaderToMetaKey:
    def test_must_return_none_when_no_header_is_provided(self):
        assert convert_header_to_meta_key(header=None) is None

    def test_must_parse_header(self):
        assert convert_header_to_meta_key(header="some-header") == "HTTP_SOME_HEADER"
