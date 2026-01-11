import logging


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class HTTPRequest:
    def __init__(
        self, url: str, method: str, headers=None, body: str = None, timeout=30
    ):
        self.url = url
        self.method = method
        self.headers = headers if headers is not None else {}
        if body is None:
            self.body = ""  # Если боди None, то будет равен пустой строке
        elif isinstance(body, str):
            self.body = body  # Если body является аргументом str, то будет равен тому, что передаст пользователь
        else:
            raise TypeError("Body должен быть или строкой или None")
        self.timeout = timeout


class HTTPRequestBuilder:
    def __init__(self):
        self._url = None
        self._method = None
        self._headers = {}
        self._body = None
        self._timeout = 30

    def set_url(self, url: str):
        if not isinstance(url, str):
            raise TypeError("URL должен быть строкой")
        if not url.startswith(("http://", "https://")):
            raise ValueError("URL должен начинаться с http:// или с https://")
        self._url = url
        return self

    def set_method(self, method: str):
        if method.upper() not in {"GET", "POST", "PUT", "DELETE", "PATCH"}:
            raise ValueError(
                "Вы указали не метод HTTP, нужно указать один из: POST, GET, PUT, DELETE, PATCH"
            )
        self._method = method.upper()
        return self

    def add_header(self, key: str, value: str):
        if isinstance(key, str) and isinstance(value, str):
            self._headers[key] = value
        return self

    def set_body(self, body: str):
        if body is not None and not isinstance(body, str):
            raise TypeError("Должна быть передана строка")
        self._body = body
        return self

    def set_timeout(self, timeout: float):
        if isinstance(timeout, (int, float)) and timeout > 0:
            self._timeout = timeout
        return self

    def build(self):
        if self._url is None or self._method is None:
            raise ValueError("url и method должны быть пррописаны")
        return HTTPRequest(
            url=self._url,
            method=self._method,
            headers=self._headers,
            body=self._body,
            timeout=self._timeout,
        )


class ValidationDecorator:
    def __init__(self, builder):
        self._builder = builder

    def set_url(self, url: str):
        if not isinstance(url, str):
            raise TypeError("Должна быть передана строка")
        if not url.startswith(("http://", "https://")):
            raise ValueError("URL должен начинаться с http:// или с https://")
        return self._builder.set_url(url)

    def set_method(self, method: str):
        if method.upper() not in {"GET", "POST", "PUT", "DELETE", "PATCH"}:
            raise ValueError(
                "Вы указали не метод HTTP, нужно указать один из: POST, GET, PUT, DELETE, PATCH"
            )
        return self._builder.set_method(method)

    def add_header(self, key: str, value: str):
        if not isinstance(key, str) or not isinstance(value, str):
            raise TypeError("Ключ и значение должны быть строкой")
        return self._builder.add_header(key, value)

    def set_body(self, body: str | None):
        if body is not None and not isinstance(body, str):
            raise ValueError("Должна быть передана строка")
        return self._builder.set_body(body)

    def set_timeout(self, timeout: int | float):
        return self._builder.set_timeout(timeout)

    def build(self):
        return self._builder.build()


class LoggingDecorator:
    def __init__(self, builder):
        self._builder = builder

    def set_url(self, url: str):
        logging.info(f"Настройки url: {url}")
        return self._builder.set_url(url)

    def set_method(self, method: str):
        logging.info(f"Передан метод {method}")
        return self._builder.set_method(method)

    def add_header(self, key: str, value: str):
        logging.info(f"Переданы значения: ключ {key}, значение {value}")
        return self._builder.add_header(key, value)

    def set_body(self, body):
        logging.info(f"Передано {body}")
        return self._builder.set_body(body)

    def set_timeout(self, timeout):
        logging.info(f"Установлен таймаут {timeout} секунд")
        return self._builder.set_timeout(timeout)

    def build(self):
        return self._builder.build()


builder = HTTPRequestBuilder()

decorator_builder = LoggingDecorator(ValidationDecorator(builder=builder))


request = (
    decorator_builder.set_url("https://api.ipify.org/?format=json")
    .set_method("GET")
    .add_header("My_IP", "json")
    .set_body("{'name': 'Ivan'}")
    .set_timeout(10)
    .build()
)

