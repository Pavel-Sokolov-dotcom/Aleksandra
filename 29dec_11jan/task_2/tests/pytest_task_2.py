import pytest
from task_2.task_2 import Student, save_students_to_json, load_students_from_json


def test_create_student():
    Ivan = Student("Ivan", 1)

    assert Ivan.student_name == "Ivan"
    assert Ivan.id == 1
    assert Ivan.subjects_marks == {}
    Ivan.add_subject("Математика")
    assert "Математика" in Ivan.subjects_marks


def test_add_subject_dublicate():
    Ivan = Student("Ivan", 1)

    Ivan.add_subject("Математика")  # Здесь я добавляю Математику в список предметов
    with pytest.raises(ValueError, match="Предмет Математика уже есть"):
        Ivan.add_subject("Математика")  # А здесь проверяю, что дубликат не запишется


def test_add_subject_empty():
    Ivan = Student("Ivan", 1)

    with pytest.raises(ValueError, match="Название предмета должно быть не пустым"):
        Ivan.add_subject("")


def test_remove_another_subject():
    Sergey = Student("Sergey", 2)
    Sergey.add_subject("Химия")
    with pytest.raises(
        ValueError, match="Такого предмета Литература нет, укажите другой предмет"
    ):
        Sergey.remove_subject("Литература")


def test_remove_nonexistent_subject():
    Sergey = Student("Sergey", 2)
    with pytest.raises(
        ValueError, match="Такого предмета Физика нет, укажите другой предмет"
    ):
        Sergey.remove_subject("Физика")


def test_add_mark_to_subjiect():
    Ekaterina = Student("Екатерина", 3)
    Ekaterina.add_subject("Физика")
    Ekaterina.add_grade("Физика", 5)
    assert Ekaterina.subjects_marks == {"Физика": [5]}


def test_add_grade():
    Elena = Student("Елена", 4)
    Elena.add_subject("Труды")
    with pytest.raises(ValueError, match="Оценка должна быть от 1 до 5 включительно"):
        Elena.add_grade("Труды", 6)

    with pytest.raises(ValueError, match="Оценка должна быть от 1 до 5 включительно"):
        Elena.add_grade("Труды", 0)

    with pytest.raises(TypeError, match="Оценка должна быть целым числом"):
        Elena.add_grade("Труды", "5")

    with pytest.raises(ValueError, match="Такого предмета Химия нет"):
        Elena.add_grade("Химия", 5)


def test_add_grade_some_marks():
    Vlad = Student("Влад", 5)
    Vlad.add_subject("Физкультура")
    Vlad.add_grade("Физкультура", 4)
    Vlad.add_grade("Физкультура", 5)
    Vlad.add_grade("Физкультура", 3)
    assert Vlad.subjects_marks["Физкультура"] == [4, 5, 3]


def test_get_gpa():
    Konstantin = Student("Константин", 6)
    Konstantin.add_subject("География")
    Konstantin.add_grade("География", 4)
    Konstantin.add_grade("География", 5)
    assert Konstantin.get_gpa() == 4.5

    Konstantin.add_subject("Обществознание")
    Konstantin.add_grade("Обществознание", 3)
    Konstantin.add_grade("Обществознание", 5)
    assert (
        Konstantin.get_gpa() == 4.25
    )  # По всем оценкам Константина 4 + 5 + 3 + 5 = 17 / 4 = 4.25

    Vladislav = Student("Владислав", 7)
    Vladislav.add_subject("Русский язык")
    assert Vladislav.get_gpa() == 0.0

    Vladimir = Student("Владимир", 8)
    assert Vladimir.get_gpa() == 0.0


def test_str():
    Olga = Student("Olga", 8)
    Olga.add_subject("Биология")
    Olga.add_grade("Биология", 5)
    Olga.add_subject("ОБЖ")
    Olga.add_grade("ОБЖ", 4)
    result = str(Olga)
    assert "Имя студента: Olga" in result
    assert "ID (8)" in result
    assert "Биология: [5]" in result
    assert "ОБЖ: [4]" in result
    assert "Средний бал по всем предметам: 4.50" in result


def test_to_dict():
    Elena = Student("Olga", 8)
    Elena.add_subject("Химия")
    Elena.add_grade("Химия", 5)
    result = Elena.to_dict()
    assert Elena.student_name == result["name"]
    assert Elena.id == result["id"]
    assert Elena.subjects_marks == result["subjects_marks"]
    assert isinstance(result, dict)


def test_from_dict():
    Dmitriy = Student("Дмитрий", 8)
    Dmitriy.add_subject("Химия")
    Dmitriy.add_grade("Химия", 5)
    result = Dmitriy.to_dict()
    copy_student = Student.from_dict(result)
    assert copy_student.student_name == Dmitriy.student_name
    assert copy_student.id == Dmitriy.id
    assert copy_student.subjects_marks == Dmitriy.subjects_marks


def test_save_load_json_file(tmp_path):
    json_file = tmp_path / "test.json"
    students = []

    Oleg = Student("Олег", 9)
    Oleg.add_subject("Информатика")
    Oleg.add_grade("Информатика", 5)
    students.append(Oleg)

    Stanislav = Student("Станислав", 10)
    Stanislav.add_subject("Природоведенье")
    Stanislav.add_grade("Природоведенье", 4)
    students.append(Stanislav)

    save_students_to_json(students, json_file)
    loaded = load_students_from_json(json_file)
    assert len(loaded) == len(students)
    for origin, load in zip(students, loaded):
        assert origin.student_name == load.student_name
        assert origin.id == load.id
        assert origin.subjects_marks == load.subjects_marks
