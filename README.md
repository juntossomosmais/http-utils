# Http Utils

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/juntossomosmais/http-utils/blob/master/LICENSE)

A simple requests session wrapper.

## Installation

`pip install pip install git+git://github.com/juntossomosmais/http-utils.git`

## Configuration process

If needed you can provide some settings as environment variables.

```text
HTTP_RETRIES=3
HTTP_BACKOFF_FACTOR=0.1
HTTP_STATUS_FORCELIST=
HTTP_TIMEOUT=30
```

## Usage

The basic usage is to call the `request_session` as a context manager.

```python
from http_utils.session import request_session


def awesome_request():
    with request_session() as request:
        response = request.get(url="https://www.some-awesome-service.com")
    return response
```
This will add:
- A retry mechanism of 3 attempts for status codes
(defined in the `HTTP_RETRIES` variable or as the `total` parameter)
- A backoff factor for each retry in seconds
(defined in the `HTTP_BACKOFF_FACTOR` variable or as the `backoff_factor` parameter)
- A list of status to force retries
(defined in the `HTTP_STATUS_FORCELIST` variable or as the `status_forcelist` parameter)
- A list of allowed methods to request
(Defined as ["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE"] methods by default or as the `allowed_methods` parameter)
- A list of hooks
(The default hooks used are the `raise_for_status` and a DEBUG level log for the response body, header and status code)

### Helpers

There are also some helper functions that can be used to parse the response object

- get_response_body: Attemps to return a parsed json response body, returning the response text if it can't.

- convert_header_to_meta_key: Converts the Django Http Request META header to be separated with a `-` instead of `_`

## Tests

In order to execute tests, execute the following:

```bash
docker-compose up -d tests
```

This will run the tests in the python 3.9.4, 3.8.5, 3.7.5, 3.6.9 tox environments
