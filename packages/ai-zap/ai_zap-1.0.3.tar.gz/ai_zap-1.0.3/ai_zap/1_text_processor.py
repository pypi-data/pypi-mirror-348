"""
Задание 1: Обработка текста
Программа удаляет повторяющиеся слова в тексте (не учитывая регистр), 
сохраняя порядок слов.
"""

def remove_duplicate_words(text):
    # Разбиваем текст на слова
    words = text.split()
    
    # Создаем список для хранения уникальных слов (с сохранением порядка)
    unique_words = []
    
    # Создаем множество для отслеживания слов, которые уже встречались
    seen_words = set()
    
    # Перебираем все слова
    for word in words:
        # Приводим слово к нижнему регистру для сравнения
        word_lower = word.lower()
        
        # Если слово еще не встречалось, добавляем его в результат
        if word_lower not in seen_words:
            unique_words.append(word)
            seen_words.add(word_lower)
    
    # Объединяем слова обратно в текст
    result = ' '.join(unique_words)
    return result

# Основная функция программы
def main():
    print("Программа для удаления повторяющихся слов в тексте")
    print("Введите текст (для завершения ввода нажмите Enter на пустой строке):")
    
    # Считываем текст построчно
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    
    # Объединяем строки в один текст
    text = ' '.join(lines)
    
    # Обрабатываем текст
    result = remove_duplicate_words(text)
    
    # Выводим результат
    print("\nТекст без повторяющихся слов:")
    print(result)

# Запускаем программу
if __name__ == "__main__":
    main() 