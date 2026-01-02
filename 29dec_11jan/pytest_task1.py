import pytest
from pathlib import Path
from task_1 import (
    reading_text,
    count_word,
    count_sentences,
    count_letters_and_digits,
    longest_word,
    show_statistics,
)

BASE_DIR = Path(__file__).parent
file_path = BASE_DIR / "text.txt"


def test_count_word():
    assert count_word("") == 0
    assert count_word("adfs , sdfsd. 24234k") == 3
    assert count_word("hi") == 1
    assert count_word("a b c d  ") == 4


def test_reading_text_string():
    assert reading_text("asdf ghj klk; rewrwe") == "asdf ghj klk; rewrwe"
    assert reading_text("text.txt") == "text.txt"
    assert reading_text("") == ""


def test_reading_text_file():
    if not file_path.exists():
        pytest.skip(f"Файл {file_path} не найден, проопускаем этот тест")
    excepted = file_path.read_text(encoding="utf-8")
    result = reading_text(str(file_path), is_filename=True)
    assert excepted == result


def test_count_sentences():
    assert count_sentences("Asadfsd. ASDDerww.") == 2
    assert count_sentences("weqwm, weqweq. eqweqw. pioioi.") == 3
    assert count_sentences("") == 0


def test_count_letters_and_digits():
    assert count_letters_and_digits("a23") == (1, 2)
    assert count_letters_and_digits("a23 fdfd33 adfsdf") == (11, 4)
    assert count_letters_and_digits("1234") == (0, 4)
    assert count_letters_and_digits("qwerty") == (6, 0)
    assert count_letters_and_digits("!,.a 3425jkj,") == (4, 4)


def test_longest_word():
    assert longest_word("asd qwerty jkl") == "qwerty"
    assert longest_word("Hello Python world") == "Python"
    assert longest_word("asd.dfdf ., qwerty,") == "qwerty"
    assert longest_word("aaaaa bbbbbb cccccccccc1") == "cccccccccc1"
    assert longest_word("asd jkl") == "asd"


def test_show_statistics(capfd):
    show_statistics(
        "asdf gfdgd 345.", source="test"
    )  # В этом тесте есть и точка и все данные для проверки моих функций
    output = capfd.readouterr().out

    assert "Статистика по test:" in output
    assert "Количество слов: 3" in output
    assert "Количество предложений: 1" in output
    assert "Самое длинное слово: gfdgd" in output
    assert "Количество букв: 9" in output
    assert "Количество цифр: 3" in output

    show_statistics(
        "asdf gfdgd 345", source="test"
    )  # В этом тест нет точки. Значит здесь 0 предложений.
    output = (
        capfd.readouterr().out
    )  # Это специальная и удобная возможность Pytest выводить несколько строк, если будет не return, а много принтов

    assert "Статистика по test:" in output
    assert "Количество слов: 3" in output
    assert "Количество предложений: 0" in output
    assert "Самое длинное слово: gfdgd" in output
    assert "Количество букв: 9" in output
    assert "Количество цифр: 3" in output
