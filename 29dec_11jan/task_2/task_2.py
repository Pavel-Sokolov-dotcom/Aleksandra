import logging  # импортирую модуль логирования


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)  # Настраиваю логирование, уровень INFO и формат: время, имя уровня и сообщение


class HTTPRequest:  # Создаю  класс для  запросов
    def __init__(
        self, url: str, method: str, headers=None, body: str = None, timeout=30
    ):  # В экземпляр класса нужно будет передать url, method, headers, body, timeout
        self.url = url  # Это адрес в формате строки
        self.method = method  # Это метод GET, POST  и  т.д.
        self.headers = headers if headers is not None else {}  # Заголовки в словарь
        if body is None:  # Условие
            self.body = ""  # Если боди None, то будет равен пустой строке
        elif isinstance(body, str):
            self.body = body  # Если body является аргументом str, то будет равен тому, что передаст пользователь
        else:
            raise TypeError("Body должен быть или строкой или None")  # Вызов ошибки
        self.timeout = timeout  # Передаётся таймаут


class HTTPRequestBuilder:  # Класс создание запроса
    def __init__(self):
        self._url = None
        self._method = None
        self._headers = {}
        self._body = None
        self._timeout = 30

    def set_url(self, url: str):  # Метод установки  url
        if not isinstance(url, str):  # Если не строка
            raise TypeError("URL должен быть строкой")  # Вызов ошибки
        if not url.startswith(
            ("http://", "https://")
        ):  # Если начинается не с http://, https://
            raise ValueError(
                "URL должен начинаться с http:// или с https://"
            )  # Вызов  ошибки
        self._url = url  # Атрибут экземпляра ссылается на переданный адрес
        return self  # Возвращаю сам экземпляр

    def set_method(self, method: str):  # Установка метода
        if method.upper() not in {
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "PATCH",
        }:  # Если нет во множестве вариантов
            raise ValueError(
                "Вы указали не метод HTTP, нужно указать один из: POST, GET, PUT, DELETE, PATCH"
            )  #  Вызов  ошибки
        self._method = method.upper()  # Ссылается  на один из прописанных методов
        return self  # Возвращаю сам экземпляр

    def add_header(
        self, key: str, value: str
    ):  # Это метод добавления заголовка с ключом и значением для словаря, как в json
        if isinstance(key, str) and isinstance(
            value, str
        ):  # Если переданные значения строки, то добавятся
            self._headers[key] = value  # Сам добавление значений
        return self  # Возвращаю экземпляр класса с новыми данными

    def set_body(self, body: str):  # Метод установки "тела"
        if body is not None and not isinstance(
            body, str
        ):  # Проверка, что тело не None и строка
            raise TypeError("Должна быть передана строка")  # Вызов ошибки
        self._body = body  # Установка значения тела
        return self  # Возвращаю экземпляр класса

    def set_timeout(self, timeout: int | float):  # Метод установки перерыва
        if (
            isinstance(timeout, (int, float)) and timeout > 0
        ):  # Проверяю, что передано число или число с плавающей точкой
            self._timeout = timeout  # Устанавливаю значение таймаута
        return self  # Возварщаю экземпляр класса

    def build(self):  # Метод сборки
        if (
            self._url is None or self._method is None
        ):  # Проверяю если пустые значения, то будет ошика
            raise ValueError("url и method должны быть пррописаны")  # Вызов ошибки
        return HTTPRequest(
            url=self._url,
            method=self._method,
            headers=self._headers,
            body=self._body,
            timeout=self._timeout,
        )  # Возвращаю запрос со всеми переданными значениями


class ValidationDecorator:  # Это  класс  валидатор, ещё это класс. Он проверяет валидность переданных данных
    def __init__(self, builder):
        self._builder = builder  # Это будет сборщик в экземпляре класса

    def set_url(self, url: str):  # Метод для проверки адреса
        if not isinstance(url, str):  # Если не строка, то будет ошибка
            raise TypeError("Должна быть передана строка")  # Вызов ошибки
        if not url.startswith(
            ("http://", "https://")
        ):  # Если начинается не с того, что ожидается
            raise ValueError(
                "URL должен начинаться с http:// или с https://"
            )  # Вызов ошибки
        return self._builder.set_url(url)  # Возвращаю через декоратор адрес сайта

    def set_method(self, method: str):  # Метод декоратора для проверки HTTP метода
        if method.upper() not in {
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "PATCH",
        }:  # Если нет во множестве нужного методы будет ошибка
            raise ValueError(
                "Вы указали не метод HTTP, нужно указать один из: POST, GET, PUT, DELETE, PATCH"
            )  # Вызов ошибки
        return self._builder.set_method(method)  # Возвращаю метод через декоратор

    def add_header(self, key: str, value: str):  # Добавление хедера
        if not isinstance(key, str) or not isinstance(
            value, str
        ):  # Проверка что переданные данные строкового типа
            raise TypeError("Ключ и значение должны быть строкой")  # Вызов ошибки
        return self._builder.add_header(key, value)  # Возвращаю хедер через  декоратор

    def set_body(self, body: str | None):  # Метод добавления боди
        if body is not None and not isinstance(
            body, str
        ):  # Проверяю, что не пусто и передана именно строка
            raise ValueError("Должна быть передана строка")  # Вызов ошибки
        return self._builder.set_body(
            body
        )  # Возвращаю значение боди через декоратор валидатоор

    def set_timeout(
        self, timeout: int | float
    ):  # Метод установки таймаута. Принимает или int или float
        if not isinstance(timeout, (int, float)):  # Условие что или int или float
            raise TypeError(
                "Тайм аут должен быть или целым числом или числом с плавающей точкой"
            )  # или int или float
        return self._builder.set_timeout(
            timeout
        )  # Возвращаю значение боди через декоратор валидатор

    def build(self):  # Метод сбора всех данных
        return self._builder.build()  # Возвращаю сборщик


# Декоратор логирования во всех методах берёт данные из класса валидатора
class LoggingDecorator:  # Класс для логирования. Сделал не через print
    def __init__(self, builder):  # Инициализация сборщика экземпляра класса
        self._builder = builder  # Ссылка на переданный сборщик

    def set_url(self, url: str):  # Метод добавления адреса сайта
        logging.info(
            f"Настройки url: {url}"
        )  # Лог об  адресе, правильно ли его передали
        return self._builder.set_url(url)  # Возарщаю сборщик

    def set_method(self, method: str):  # Метод установки метода
        logging.info(
            f"Передан метод {method}"
        )  # Лог об успешной или не успешной передачи метода
        return self._builder.set_method(method)  # Возвращаю метод

    def add_header(self, key: str, value: str):  # Метод добавления хедера
        logging.info(
            f"Переданы значения: ключ {key}, значение {value}"
        )  # Выведет параметры
        return self._builder.add_header(key, value)  # Возвращаю переданные параметры

    def set_body(self, body):  # Метод установки тела запроса
        logging.info(f"Передано {body}")  # Лог об body
        return self._builder.set_body(body)  # Возвращаю установленное тело запроса

    def set_timeout(self, timeout):  # Метод установки таймаута
        logging.info(
            f"Установлен таймаут {timeout} секунд"
        )  # Лог об установлении таймаута
        return self._builder.set_timeout(timeout)  # Возвращаю значение таймаута

    def build(self):  # Собираю весь запрос
        return self._builder.build()  # Возвращаю запрос целиком
