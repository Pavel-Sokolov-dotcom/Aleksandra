from collections import Counter
import json


class Book:
    def __init__(
        self,
        name: str,
        isbn: str,
        author: str,
        genre: str,
        year: int,
        is_available=True,
    ):  # Если is_available=True значит книга в библиотеке, доступна для выдачи
        self.name = name
        self.isbn = isbn
        self.author = author
        self.genre = genre
        self.year = year
        self.is_available = is_available
        self.current_reader = None

    def issue_book(self, reader_name):
        """
        Метод для выдачи книги из библиотеки
        """
        if (
            not self.is_available
        ):  # Если у книги статус False, то есть не True, значит книги нет в библиотеке
            raise ValueError(
                f"Книга выдана читателю {self.current_reader}"
            )  # Вызываю ошибку
        else:
            self.is_available = (
                False  # Меняю статус книги на такой, что можно выдать книгу читателю
            )
            self.current_reader = reader_name  # В экземпляре класса у текущего читателя обновляется читатель
        return self.current_reader

    def return_book(self):
        """
        Метод для возврата книги в библиотеку
        """
        if self.is_available:
            raise ValueError(f"Книга уже находится в библиотеке")
        else:
            self.is_available = True
        self.current_reader = None

    def __str__(self):
        """
        Метод для удобного представления информации о книге
        """
        book_status = (
            "Книга доступна для выдачи"
            if self.is_available
            else f"Книга не доступна для выдачи. Её читает {self.current_reader}"
        )
        return f"{self.name}, автор: {self.author}, жанр: {self.genre}, год: {self.year}, статус: {book_status} "

    def to_dict(self):
        """
        Метод для сохранения книги в json-формат
        """
        return {
            "name": self.name,
            "isbn": self.isbn,
            "author": self.author,
            "genre": self.genre,
            "year": self.year,
            "is_available": self.is_available,
            "current_reader": self.current_reader,
        }

    @classmethod
    def from_dict(cls, data: dict):
        book = cls(
            name=data["name"],
            isbn=data["isbn"],
            author=data["author"],
            genre=data["genre"],
            year=data["year"],
            is_available=data["is_available"],
        )
        book.current_reader = data.get("current_reader")
        return book


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book: Book):
        if not isinstance(book, Book):  # Проверяю, что переданна именно книга
            raise TypeError("Можно добавлять только объекты класса Book")
        self.books.append(book)

    def remove_book(self, isbn: str):
        if not isbn:
            raise ValueError("ISBN не может быть пустым")

        for index, book in enumerate(self.books):
            if book.isbn == isbn:
                del self.books[index]
                return  # Если книга найдена и удалена по индексу из списка, то вызов return прекратит цикл и выполнение метода (функции)
        raise ValueError(f"Книга по ISBN {isbn} не найдена")

    def find_book(self, isbn: str):
        if not isbn:
            raise ValueError("ISBN не может быть пустым")
        for book in self.books:
            if book.isbn == isbn:
                return book

        raise ValueError(
            f"Книга по ISBN {isbn} не найдена"
        )  # Если книга не найдена, то вызываю ошибку

    def issue_book(self, isbn: str, reader_name: str):
        book = self.find_book(isbn)
        return book.issue_book(reader_name)

    def return_book(self, isbn):
        book = self.find_book(isbn)
        book.return_book()

    def get_statistics(self):
        genre = Counter(book.genre for book in self.books)
        year = Counter(book.year for book in self.books)
        return genre, year

    def save_to_json(self, filename):
        library_list = (
            []
        )  # можно более компактно через лист компрехеншн [book.to_dict() for book in self.books]
        for book in self.books:
            library_list.append(book.to_dict())
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(library_list, file, ensure_ascii=False, indent=2)

    @classmethod
    def load_from_json(cls, filename):
        library = cls()
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                for item in data:
                    book = Book.from_dict(item)
                    library.books.append(book)
        except FileNotFoundError:
            raise ValueError(f"Файл {filename} не найден")
        return library
