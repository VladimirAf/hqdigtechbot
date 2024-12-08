import logging

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Токен API для бота
API_TOKEN = ''

# Данные для квиза
quiz_data = [
    {
        'question': 'Что такое Python?',
        'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
        'correct_option': 0
    },
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'natural'],
        'correct_option': 0
    },
    {
        'question': 'Какой метод используется для добавления элемента в список?',
        'options': ['append()', 'add()', 'insert()', 'push()'],
        'correct_option': 0
    },
    {
        'question': 'Какой результат у выражения 5 // 2 в Python?',
        'options': ['2', '2.5', '1', '5.2'],
        'correct_option': 0
    },
    {
        'question': 'Какая функция используется для получения длины строки?',
        'options': ['len()', 'size()', 'length()', 'count()'],
        'correct_option': 0
    },
    {
        'question': 'Какой оператор используется для проверки равенства?',
        'options': ['==', '=', '!=', '==='],
        'correct_option': 0
    },
    {
        'question': 'Что делает метод .split() в Python?',
        'options': ['Разделяет строку на части', 'Объединяет строки', 'Удаляет пробелы', 'Переводит строку в верхний регистр'],
        'correct_option': 0
    },
    {
        'question': 'Какая функция используется для преобразования строки в целое число?',
        'options': ['int()', 'float()', 'str()', 'eval()'],
        'correct_option': 0
    },
    {
        'question': 'Какой модуль используется для работы с рандомными числами?',
        'options': ['random', 'math', 'os', 'sys'],
        'correct_option': 0
    },
    {
        'question': 'Что возвращает функция range(5)?',
        'options': ['Итератор', 'Список [0, 1, 2, 3, 4]', 'Число 5', 'Кортеж'],
        'correct_option': 0
    }
]
