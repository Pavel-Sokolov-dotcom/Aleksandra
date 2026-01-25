import pytest
from task_3.task_3 import Book, Library
from pathlib import Path


def test_book():
    """
    Проверяю что объект книги создаётся
    """
    book_1 = Book("1984", "123", "Orwell", "Dystopia", 1949)
    assert book_1.name == "1984"
    assert book_1.current_reader == None
    assert book_1.genre == "Dystopia"
    assert book_1.isbn == "123"
    assert book_1.is_available is True


def test_issue_and_return():
    """
    Проверяю выдачу книги
    """
    book_2 = Book("Test", "111", "Author", "Fiction", 2020)
    book_2.issue_book("Ekaterina")  # Выдаю книгу Екатерине
    assert book_2.is_available is False  # Книга выдана
    assert book_2.current_reader == "Ekaterina"  # Книга выдана Екатерине

    book_2.return_book()  # Возврат книги
    book_2.is_available == True  # Статус книги поменялся, теперь книга в библиотеке
    book_2.current_reader is None  # Читателя у книги снова нет


def test_error_issue():
    """
    Проверяю, что будет вызвана ошибка при другом имени
    """
    book_3 = Book("Руслан и Людмила", "0111", "А.С. Пушкин", "Роман", 1818)
    book_3.issue_book("Ivan")  # Выдаю книгу Ивану
    with pytest.raises(ValueError, match="выдана"):
        book_3.issue_book("Ivan")


def test_error_return():
    """
    Проверяю, что будет вызвана ошибка при другом статусе
    """
    book_4 = Book("Парус", "0112", "М.Ю. Лермонтов", "Стихотворение", 1841)
    with pytest.raises(
        ValueError, match="Книга уже находится в библиотеке"
    ):  # match это совпадение текста с текстом ошибки
        book_4.return_book()


def test_to_dict_from_dict():
    """
    Проверяю загрузку из словаря
    """
    book_5 = Book("Алиса в Стране чудес", "023", "Льюис Кэрролл", "Роман", 1865)
    book_5.issue_book("Alisa")

    data = book_5.to_dict()
    restor = Book.from_dict(data)

    assert restor.name == book_5.name
    assert restor.author == book_5.author
    assert restor.genre == book_5.genre
    assert restor.current_reader == book_5.current_reader


def test_library():
    """
    Проверяю работу класса Library
    """
    lib_1 = Library()
    book_6 = Book("Война и мир", "024", "Лев Толстой", "Роман", 1865)

    lib_1.add_book(book_6)
    find = lib_1.find_book("024")
    assert find is book_6


def test_temp_json(tmp_path):
    """
    Проверяю работу временного файла json
    """
    json_file = tmp_path / "library.json"
    lib_2 = Library()
    lib_2.add_book(
        Book("Преступление и наказание", "025", "Фёдор Достоевский", "Роман", 1866)
    )
    lib_2.issue_book("025", "Sergey")
    lib_2.save_to_json(json_file)

    lib_3 = Library.load_from_json(json_file)
    book_7 = lib_3.find_book("025")

    assert book_7.name == "Преступление и наказание"
    assert book_7.is_available is False
    assert book_7.current_reader == "Sergey"


def test_load_manual_json():
    """
    Проверяю работу файла json из директории
    """
    TEST_DIR = Path(__file__).parent
    json_path = TEST_DIR / "library.json"
    lib = Library.load_from_json(json_path)
    book = lib.find_book("025")

    assert book.name == "Преступление и наказание"
