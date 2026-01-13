import pytest
from task_1.task_1 import count_symbols


def test_positive_only_letters():
    assert count_symbols("qwertyy") == "Букв: 7, цифр: 0, пробелов: 0"
    assert count_symbols("Ffa") == "Букв: 3, цифр: 0, пробелов: 0"
    assert count_symbols("FfaA") == "Букв: 4, цифр: 0, пробелов: 0"


def test_positive_only_digits():
    assert count_symbols("123,.") == "Букв: 0, цифр: 3, пробелов: 0"
    assert count_symbols("7890000") == "Букв: 0, цифр: 7, пробелов: 0"


def test_positive_only_spaces():
    assert count_symbols("    !,.") == "Букв: 0, цифр: 0, пробелов: 4"
    assert count_symbols("    .  ") == "Букв: 0, цифр: 0, пробелов: 6"


def test_consist_all():
    assert count_symbols("A a 1 . b") == "Букв: 3, цифр: 1, пробелов: 4"
    assert count_symbols("asd$ S  !  789") == "Букв: 4, цифр: 3, пробелов: 5"
