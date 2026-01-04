import json


class Student:
    def __init__(self, name: str, id: int):
        self.student_name = name
        self.id = id
        self.subjects_marks = {}
    
    def add_subject(self, subject):
        if not isinstance(subject, str) or not subject.strip():
            raise ValueError("Название предмета должно быть не пустым")
        subject = subject.strip()
        
        if subject in self.subjects_marks:
            raise ValueError(f"Предмет {subject} уже есть")
        self.subjects_marks[subject] = [] # Добавляю предмет в словарь и значением пустой список для оценок 
        
    def remove_subject(self, subject):
        if not isinstance(subject, str) or not subject.strip():
            raise ValueError("Название предмета должно быть не пустым")
        subject = subject.strip()
        
        
        if subject not in self.subjects_marks:
            raise ValueError(f"Такого предмета {subject} нет, укажите другой предмет")
        else:
            self.subjects_marks.pop(subject) # Удаляю предмет вместе с оценками
        
    def add_grade(self, subject: str, mark: int):
        if not isinstance(subject, str) or not subject.strip():
            raise ValueError("Название не должно быть пустым")
        
        if subject not in self.subjects_marks:
            raise ValueError(f"Такого предмета {subject} нет")
        
        if not isinstance(mark, int):
            raise TypeError("Оценка должна быть целым числом")
        if not (1 <= mark <= 5):
            raise ValueError("Оценка должна быть от 1 до 5 включительно")
        
        self.subjects_marks[subject].append(mark)


    def get_gpa(self):
        avg_all_marks = []
        for mark in self.subjects_marks.values():
            avg_all_marks.extend(mark)
        if len(avg_all_marks) == 0:
            return 0.0
        
        return sum(avg_all_marks) / len(avg_all_marks)
    
    def __str__(self):
        if  self.subjects_marks:
            subjects_lines = "\n ".join(
                f"- {subject}: {marks}"
                for subject, marks in self.subjects_marks.items()
            )
            subjects_info = f"Список предметов:\n {subjects_lines}"
        else:
            subjects_info = "Предметов нет"
        return (
            f"Имя студента: {self.student_name} ID ({self.id})\n"
            f"{subjects_info}\n"
            f"Средний бал по всем предметам: {self.get_gpa():.2f}"
        )
    
    def to_dict(self):
        return {
            "name": self.student_name,
            "id": self.id,
            "subjects_marks": self.subjects_marks
        }
        
    @classmethod
    def from_dict(cls, data): # Это json converter
        student = cls(data["name"], data["id"])
        student.subjects_marks = data["subjects_marks"]
        return student
    

def save_students_to_json(students: list, filename: str):
    list_of_students = []
    for student in students:
        list_of_students.append(student.to_dict())
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(list_of_students, f, ensure_ascii=False, indent=2)


def load_students_from_json(filename: str):
    students_list = []
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data:
            students_list.append(Student.from_dict(item))
    return students_list

