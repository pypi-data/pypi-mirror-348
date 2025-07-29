from openai import OpenAI
import os

def zap(text, api_key="64ef86312b5b4226a2eced79eb640b79"):
    """
    Отправляет запрос к ИИ и возвращает ответ.
    
    Args:
        text (str): Текст запроса
        api_key (str): API ключ для доступа к сервису
        
    Returns:
        str: Ответ от ИИ
    """
    client = OpenAI(
        base_url="https://api.aimlapi.com/v1",
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model="Qwen/Qwen3-235B-A22B-fp8-tput",
        messages=[
            {
                "role": "system",
                "content": "Ты - помощник, который даёт чёткие и точные ответы. Не показывай процесс размышления, сразу давай правильный ответ. Если это математическая задача, покажи формулу и вычисления. Если это вопрос по программированию, давай готовый код. Если это общий вопрос, давай краткий и информативный ответ."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.3,
        top_p=0.8,
        frequency_penalty=0.5,
        max_tokens=4096,
    )

    return response.choices[0].message.content 

def otv(query=None):
    """
    Выводит ответы на теоретические вопросы.
    
    Параметры:
    - query: номер вопроса, текст для поиска или '?' для списка вопросов
    
    Возвращает:
    - Строку с ответом или списком вопросов
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'otv.txt')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Разделяем на вопросы и ответы
        qa_pairs = []
        current_question = None
        current_answer = []
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Если строка начинается с цифры и точки - это новый вопрос
            if line[0].isdigit() and '. ' in line:
                if current_question is not None:
                    qa_pairs.append((current_question, '\n'.join(current_answer)))
                current_question = line
                current_answer = []
            else:
                if current_question is not None:
                    current_answer.append(line)
        
        # Добавляем последнюю пару
        if current_question is not None:
            qa_pairs.append((current_question, '\n'.join(current_answer)))
        
        if query is None:
            # Выводим все ответы
            return '\n\n'.join(f"{q}\n{a}" for q, a in qa_pairs)
        elif query == '?':
            # Выводим список вопросов
            return '\n'.join(q for q, _ in qa_pairs)
        elif isinstance(query, (int, str)):
            # Ищем по номеру или тексту
            if isinstance(query, int):
                # Поиск по номеру
                for q, a in qa_pairs:
                    if q.startswith(f"{query}."):
                        return f"{q}\n{a}"
                return f"Вопрос {query} не найден"
            else:
                # Поиск по тексту
                found = []
                for q, a in qa_pairs:
                    if query.lower() in q.lower() or query.lower() in a.lower():
                        found.append(f"{q}\n{a}")
                if found:
                    return '\n\n'.join(found)
                return f"По запросу '{query}' ничего не найдено"
        else:
            return "Неверный формат запроса"
            
    except Exception as e:
        return f"Ошибка при чтении файла: {str(e)}"

def zad(query=None):
    """
    Функция для работы с практическими заданиями.
    
    Args:
        query: Может быть:
            - None: выводит список заданий
            - число (1-5): создает файл с решением задания
    
    Returns:
        str: Информация о заданиях или результат создания файла
    """
    tasks = {
        1: {
            'name': 'Обработка текста',
            'description': 'Программа удаляет повторяющиеся слова в тексте (не учитывая регистр), сохраняя порядок слов.',
            'file': '1_text_processor.py'
        },
        2: {
            'name': 'Работа с файлами',
            'description': 'Программа запрашивает у пользователя строку, записывает её в файл, затем считывает из файла и выводит на экран.',
            'file': '2_file_io.py'
        },
        3: {
            'name': 'Создание приложения в форме как экран телефона',
            'description': 'Простое приложение, где пользователь вводит текст, нажимает кнопку, и текст меняет свой шрифт на один из предопределенных вариантов.',
            'file': '3_phone_app.py'
        },
        4: {
            'name': 'Алгоритмы и структуры данных',
            'description': 'Функция, которая принимает список чисел и сортирует его по убыванию, используя алгоритм сортировки пузырьком.',
            'file': '4_bubble_sort.py'
        },
        5: {
            'name': 'Работа с классами',
            'description': 'Создание класса Student с атрибутами имя, фамилия, список оценок. Реализация метода, который возвращает средний балл студента.',
            'file': '5_student_class.py'
        }
    }
    
    if query is None or query == '?':
        # Выводим список заданий
        result = "Доступные задания:\n"
        for num, task in tasks.items():
            result += f"\n{num}. {task['name']}\n{task['description']}\n"
        return result
    
    elif isinstance(query, int):
        # Создаем файл с решением
        if query in tasks:
            try:
                # Получаем путь к директории, где находится текущий файл
                current_dir = os.path.dirname(os.path.abspath(__file__))
                source_path = os.path.join(current_dir, tasks[query]['file'])
                
                with open(source_path, 'r', encoding='utf-8') as source:
                    content = source.read()
                
                # Создаем файл в текущей директории
                with open(f'solution_{query}.py', 'w', encoding='utf-8') as target:
                    target.write(content)
                return f"Файл solution_{query}.py создан успешно"
            except Exception as e:
                return f"Ошибка при создании файла: {e}"
        return f"Задание с номером {query} не найдено"
    
    elif isinstance(query, str) and query.isdigit():
        # Если строка содержит число, преобразуем в int
        num = int(query)
        if num in tasks:
            try:
                # Получаем путь к директории, где находится текущий файл
                current_dir = os.path.dirname(os.path.abspath(__file__))
                source_path = os.path.join(current_dir, tasks[num]['file'])
                
                with open(source_path, 'r', encoding='utf-8') as source:
                    content = source.read()
                
                # Создаем файл в текущей директории
                with open(f'solution_{num}.py', 'w', encoding='utf-8') as target:
                    target.write(content)
                return f"Файл solution_{num}.py создан успешно"
            except Exception as e:
                return f"Ошибка при создании файла: {e}"
        return f"Задание с номером {num} не найдено"
    
    return "Неверный формат запроса" 