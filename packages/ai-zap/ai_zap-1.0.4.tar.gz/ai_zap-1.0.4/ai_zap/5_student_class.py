"""
Задание 5: Работа с классами
Создание класса Student с атрибутами имя, фамилия, список оценок.
Реализация метода, который возвращает средний балл студента.
"""

class Student:
    """
    Класс, представляющий студента с именем, фамилией и списком оценок.
    """
    
    def __init__(self, first_name, last_name, grades=None):
        """
        Инициализация объекта Student.
        
        Параметры:
        - first_name: имя студента
        - last_name: фамилия студента
        - grades: список оценок (по умолчанию пустой список)
        """
        self.first_name = first_name
        self.last_name = last_name
        self.grades = grades if grades is not None else []
    
    def add_grade(self, grade):
        """
        Добавление новой оценки в список оценок студента.
        
        Параметры:
        - grade: новая оценка (число)
        """
        # Проверяем, что оценка является числом
        if isinstance(grade, (int, float)):
            self.grades.append(grade)
        else:
            print("Ошибка: оценка должна быть числом.")
    
    def get_average_grade(self):
        """
        Вычисляет и возвращает средний балл студента.
        
        Возвращает:
        - средний балл или 0, если нет оценок
        """
        if not self.grades:
            return 0
        
        # Вычисляем средний балл
        return sum(self.grades) / len(self.grades)
    
    def get_full_name(self):
        """
        Возвращает полное имя студента.
        """
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        """
        Возвращает строковое представление студента.
        """
        return f"Студент: {self.get_full_name()}, Средний балл: {self.get_average_grade():.2f}"


def main():
    print("Программа для работы с классом Student")
    
    # Создаем студентов
    student1 = Student("Иван", "Иванов", [4, 5, 3, 5, 4])
    student2 = Student("Мария", "Петрова")
    
    # Добавляем оценки второму студенту
    student2.add_grade(5)
    student2.add_grade(5)
    student2.add_grade(4)
    
    # Выводим информацию о студентах
    print("\nИнформация о студентах:")
    print(student1)
    print(f"Список оценок: {student1.grades}")
    
    print("\n" + str(student2))
    print(f"Список оценок: {student2.grades}")
    
    # Демонстрация интерактивного создания студента
    print("\nСоздание нового студента:")
    first_name = input("Введите имя студента: ")
    last_name = input("Введите фамилию студента: ")
    
    new_student = Student(first_name, last_name)
    
    # Ввод оценок
    print("Введите оценки студента (для завершения введите 'готово'):")
    while True:
        grade_input = input("Оценка: ")
        if grade_input.lower() == 'готово':
            break
        
        try:
            grade = float(grade_input)
            new_student.add_grade(grade)
        except ValueError:
            print("Ошибка: введите число или 'готово' для завершения.")
    
    # Вывод информации о новом студенте
    print("\nИнформация о новом студенте:")
    print(new_student)
    print(f"Список оценок: {new_student.grades}")


# Запускаем программу
if __name__ == "__main__":
    main() 