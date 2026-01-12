import pytest
from task_2.task_2 import (
    HTTPRequestBuilder,
    ValidationDecorator,
    LoggingDecorator,
)


def test_positive_right_answer():
    builder = HTTPRequestBuilder()
    decorator_builder = LoggingDecorator(ValidationDecorator(builder))
    req = (
        decorator_builder.set_url("https://api.ipify.org/?format=json")
        .set_method("GET")
        .add_header("My_IP", "json")
        .set_body("{'name': 'Ivan'}")
        .set_timeout(10)
        .build()
    )
    assert req.url == "https://api.ipify.org/?format=json"
    assert req.method == "GET"
    assert req.body == "{'name': 'Ivan'}"
    assert req.timeout == 10
    assert req.headers == {"My_IP": "json"}
