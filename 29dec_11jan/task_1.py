import sys
from pathlib import Path
import re  # импортирую регулярные выражения, с ним удобно делать манипуляции с текстом
from typing import Tuple


# Первый позиционный аргумент text может быть и строкой и имененм файла.
# Именованный аргумент по умолчанию не файл, если передаём файл, то указываем True
def reading_text(text: str = None, is_filename: bool = False) -> str:
    if is_filename:
        if text is None:
            raise ValueError("Путь к файлу не указан")
        try:
            return Path(text).read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"❌ Ошибка: Файл '{text}' не найден", file=sys.stderr)
            sys.exit(1)
    else:
        if text is None:
            return sys.stdin.read()
        return text


def count_word(text: str):
    words = re.findall(
        r"\b\w+\b", text
    )  # с помощью модуля re ищу только слова, отсекаю начало и конец слова, не беру симоволы знаков припенаний. words будет ссылаться на список слов.
    return len(words)  # возвращаю длину списка слов


def count_sentences(text: str):
    find_dot = re.findall(r"[.!?]+(?=\s|$)", text)
    return len(find_dot)


def longest_word(text: str):
    words = re.findall(r"\b\w+\b", text)
    return max(words, key=len) if words else ""


def count_letters_and_digits(text: str) -> Tuple[int, int]:
    letters = sum(1 for i in text if i.isalpha())
    digits = sum(1 for j in text if j.isdigit())
    return letters, digits


def show_statistics(text: str, source: str = "Входные данные") -> None:
    print(f"Статистика по {source}:")
    print(f"Количество слов: {count_word(text)}")
    print(f"Количество предложений: {count_sentences(text)}")
    print(f"Самое длинное слово: {longest_word(text)}")

    letters, digits = count_letters_and_digits(text)
    print(f"Количество букв: {letters}")
    print(f"Количество цифр: {digits}")


