import json  # Импортирую json, чтобы конвертировать, в будущем, все данные в json


class Student:  # Создаю основной класс для этой задачи
    def __init__(
        self, name: str, id: int
    ):  # Экземпляры класса будут содержать имя студента, айди и словарь предметов с оценками
        self.student_name = (
            name  # self это ссылка на экземпляр класса, будет создержать имя
        )
        self.id = id  # Здесь будет содержаться айди
        self.subjects_marks = {}  # Здесь будет словарь с предметами и оценками

    def add_subject(self, subject):  # Метод будет добавлять предмет
        if (
            not isinstance(subject, str) or not subject.strip()
        ):  # Здесь проверяю, что то, что передаёт пользователь
            # является предметом и является строкой и не разделённая строка на список
            raise ValueError(
                "Название предмета должно быть не пустым"
            )  # Если предмет не строка, то вызываю ошибку
        subject = subject.strip()  # subject ссылается на список предметов

        if (
            subject in self.subjects_marks
        ):  # Если предмет уже есть в словаре, то вызовется ошибка
            raise ValueError(f"Предмет {subject} уже есть")  # Текст ошибки
        self.subjects_marks[subject] = (
            []
        )  # Добавляю предмет в словарь и значением пустой список для оценок

    def remove_subject(self, subject):  # Этот метод будет удалять предмет
        if (
            not isinstance(subject, str) or not subject.strip()
        ):  # Если передана не строка или разделённая строка
            raise ValueError("Название предмета должно быть не пустым")  # Вызов ошибки
        subject = subject.strip()  # Предмет ссылается на список из предмета

        if (
            subject not in self.subjects_marks
        ):  # Если предмета нет  в словаре Предметов и оценок
            raise ValueError(
                f"Такого предмета {subject} нет, укажите другой предмет"
            )  # То вызываю ошибку
        else:
            self.subjects_marks.pop(subject)  # Удаляю предмет вместе с оценками

    def add_grade(self, subject: str, mark: int):  # Метод добавляет оценку к предметы
        if (
            not isinstance(subject, str) or not subject.strip()
        ):  # Проверяю, что строка и что не список
            raise ValueError("Название не должно быть пустым")  # Вызов ошибки

        if (
            subject not in self.subjects_marks
        ):  # Если предмета нет в словаре то будет ошибка
            raise ValueError(f"Такого предмета {subject} нет")  # Сама ошибка

        if not isinstance(mark, int):  # Если оценка не целое число
            raise TypeError("Оценка должна быть целым числом")  # Ошибка не верного типа
        if not (
            1 <= mark <= 5
        ):  # Здесь проверяю, чтооценка должна быть от 1 до 5 включительно
            raise ValueError(
                "Оценка должна быть от 1 до 5 включительно"
            )  # Вызов ошибки

        self.subjects_marks[subject].append(
            mark
        )  # Здесь добавляю оценку в словарь по ключу Предмета

    def get_gpa(self):  # Этот метод получения средней оценки по всем предметам
        avg_all_marks = []  # Добавляю пустой список
        for (
            mark
        ) in (
            self.subjects_marks.values()
        ):  # Прохожу циклом по значениям оценок в словаре
            avg_all_marks.extend(mark)  # Добавляю в пустой список все оценки
        if len(avg_all_marks) == 0:  # Если оценок нет то вернётся 0.0
            return 0.0  # Возврат 0.0

        return sum(avg_all_marks) / len(
            avg_all_marks
        )  # Вычисляю среднее значение и возвращаю его

    def __str__(self):  # Метод для отображения читаемой информации
        if (
            self.subjects_marks
        ):  # Если словарь не пустой, то будет буводиться информация о студентах и оценках
            subjects_lines = "\n ".join(
                f"- {subject}: {marks}"
                for subject, marks in self.subjects_marks.items()  # Здесь как лист компехеншн добавление в строку
            )  # Будет объедлинение в строку Предмет оценка, проходится циклом по всем значениям словаря
            subjects_info = f"Список предметов:\n {subjects_lines}"
        else:
            subjects_info = (
                "Предметов нет"  # Если словарь пустой, то будет выводиться сообщение
            )
        return (
            f"Имя студента: {self.student_name} ID ({self.id})\n"
            f"{subjects_info}\n"
            f"Средний бал по всем предметам: {self.get_gpa():.2f}"
        )  # Возвращаю кортеж строк

    def to_dict(self):  # Метод преобразования в словарь
        return {
            "name": self.student_name,
            "id": self.id,
            "subjects_marks": self.subjects_marks,
        }  # Возвращаю словарь студента: имя, id, предметы и оценки

    @classmethod  # Метод класса, работает с классом
    def from_dict(cls, data):  # Это json converter принимает данные
        student = cls(
            data["name"], data["id"]
        )  # Переменная сслается на Класс у которого будет имя студента и его id
        student.subjects_marks = data[
            "subjects_marks"
        ]  # Здесь словарю класса присваивается словарь предметов и оценок
        return student  # Возвращаю объект класса


def save_students_to_json(
    students: list, filename: str
):  # Функция сохранения в json формат информации о студентах
    list_of_students = []  # Объявление пустого списка
    for student in students:  # Прохожу циклом по переданным студентам
        list_of_students.append(
            student.to_dict()
        )  # Добавляю в пустой список объект студента
    with open(
        filename, "w", encoding="utf-8"
    ) as f:  # С помощью контекстного менеджера открываю файл для чтения
        json.dump(
            list_of_students, f, ensure_ascii=False, indent=2
        )  # Здесь сохраняю всё в json-формат. ensure_ascii=False чтобы Кирилица не экранировалась, отступ в json


def load_students_from_json(
    filename: str,
):  # Функция чтения данных из json и запись в список
    students_list = []  # Пустой список, в который будут добавляться словари
    with open(
        filename, "r", encoding="utf-8"
    ) as f:  # Контекстный менеджер открывает файл для чтения
        data = json.load(f)  # Переменная data ссылается на json, который читает файл
        for item in data:  # Прохожу циклом по переменной
            students_list.append(
                Student.from_dict(item)
            )  # Добавляю в пустой список данные словаря, которые извлекаются из Класса методом класса
    return students_list  # Возвращаю список словарей студентов
