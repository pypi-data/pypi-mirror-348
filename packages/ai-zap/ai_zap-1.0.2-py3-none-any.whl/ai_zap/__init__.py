from openai import OpenAI

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
    Функция для работы с ответами на теоретические вопросы.
    
    Args:
        query: Может быть:
            - None: выводит все ответы
            - число (1-52): выводит ответ под указанным номером
            - строка: ищет ответ по тексту вопроса
            - '?': выводит список вопросов с номерами
    
    Returns:
        str: Запрошенная информация
    """
    try:
        with open('otv.txt', 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        return "Файл с ответами не найден"
    
    # Разбиваем на вопросы и ответы
    qa_pairs = []
    current_qa = []
    
    for line in content.split('\n'):
        if line.strip() and not line.startswith('•') and not line.startswith('–'):
            if current_qa:
                qa_pairs.append('\n'.join(current_qa))
            current_qa = [line]
        elif line.strip():
            current_qa.append(line)
    
    if current_qa:
        qa_pairs.append('\n'.join(current_qa))
    
    # Обработка запроса
    if query is None:
        return content
    
    elif query == '?':
        # Выводим только вопросы
        questions = []
        for i, qa in enumerate(qa_pairs, 1):
            question = qa.split('\n')[0]
            questions.append(f"{i}. {question}")
        return '\n'.join(questions)
    
    elif isinstance(query, int):
        # Поиск по номеру
        if 1 <= query <= len(qa_pairs):
            return qa_pairs[query-1]
        return f"Вопрос с номером {query} не найден"
    
    elif isinstance(query, str):
        if query.isdigit():
            # Если строка содержит число, преобразуем в int
            num = int(query)
            if 1 <= num <= len(qa_pairs):
                return qa_pairs[num-1]
            return f"Вопрос с номером {num} не найден"
        else:
            # Поиск по тексту
            query = query.lower()
            for qa in qa_pairs:
                if query in qa.lower():
                    return qa
            return "Вопрос не найден"
    
    return "Неверный формат запроса"

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
                with open(tasks[query]['file'], 'r', encoding='utf-8') as source:
                    content = source.read()
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
                with open(tasks[num]['file'], 'r', encoding='utf-8') as source:
                    content = source.read()
                with open(f'solution_{num}.py', 'w', encoding='utf-8') as target:
                    target.write(content)
                return f"Файл solution_{num}.py создан успешно"
            except Exception as e:
                return f"Ошибка при создании файла: {e}"
        return f"Задание с номером {num} не найдено"
    
    return "Неверный формат запроса" 