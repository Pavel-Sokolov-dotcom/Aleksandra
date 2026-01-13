# def count_symbols(text: str) -> dict:
#     """Эта функция считает все символы в переданной строке.
#     Выводит словарь.
#     Но это не правильное решение для задачи.
#     Оставлю этот код как первую попытку решения.
#     """
#     result_dct = {}
#     for item in text:
#         result_dct[item] = text.count(item)
#     return  result_dct # Можно в одну строку {item: text.count(item) for item in text}


def count_symbols(text: str) -> str:
    if not isinstance(
        text, str
    ):  # Проверяю, что передана строка, если нет, то будет вызвана ошибка
        raise ("Вы должны передать строку")

    letters = digits = spaces = 0  # Сначала все счётчики равны нулю

    for item in text:
        if item.isalpha():  # Если буква (латинская или кириллица), то прибавляем 1
            letters += 1
        elif item.isdigit():  # Если цифра, то прибавляем 1
            digits += 1
        elif item == " ":  # Если символ это пробел, то прибавляем 1
            spaces += 1

    return f"Букв: {letters}, цифр: {digits}, пробелов: {spaces}"  # Возвращаю итоговую строку со статистикой
