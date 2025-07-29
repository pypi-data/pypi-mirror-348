"""
Задание 2: Работа с файлами
Программа запрашивает у пользователя строку, записывает её в файл,
затем считывает из файла и выводит на экран.
"""

def write_to_file(text, filename):
    """Записывает текст в файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
        return True
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")
        return False

def read_from_file(filename):
    """Считывает текст из файла"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

def main():
    print("Программа для работы с файлами")
    
    # Запрашиваем строку у пользователя
    user_text = input("Введите строку для записи в файл: ")
    
    # Имя файла для записи
    filename = "user_text.txt"
    
    # Записываем строку в файл
    if write_to_file(user_text, filename):
        print(f"Строка успешно записана в файл '{filename}'")
        
        # Считываем строку из файла
        read_text = read_from_file(filename)
        if read_text is not None:
            print("\nСодержимое файла:")
            print(read_text)
    else:
        print("Не удалось выполнить операцию.")

# Запускаем программу
if __name__ == "__main__":
    main() 