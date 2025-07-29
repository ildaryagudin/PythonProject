import pytest

from src.processing import filter_by_state, sort_by_date


# Фикстуры с примерами данных
@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELLED"},
        {"id": 3, "state": "EXECUTED"},
        {"id": 4, "state": "REJECTED"}
    ]


# Базовый тест: фильтрация по состоянию "EXECUTED"
def test_filter_default(sample_transactions):
    filtered = filter_by_state(sample_transactions)
    expected_result = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 3, "state": "EXECUTED"}
    ]
    assert filtered == expected_result


# Тестирование фильтрации по состоянию "CANCELLED"
def test_filter_cancelled(sample_transactions):
    filtered = filter_by_state(sample_transactions, "CANCELLED")
    expected_result = [{"id": 2, "state": "CANCELLED"}]
    assert filtered == expected_result


# Тестирование фильтрации по отсутствующему состоянию
def test_filter_unknown_state(sample_transactions):
    filtered = filter_by_state(sample_transactions, "UNKNOWN")
    expected_result = []
    assert filtered == expected_result


# Тестирование передачи пустого списка транзакций
def test_empty_transactions():
    empty_transactions = []
    filtered = filter_by_state(empty_transactions)
    expected_result = []
    assert filtered == expected_result


# Тестирование некорректных данных (несловарь)
def test_invalid_data_type():
    invalid_transactions = ["not a dictionary"]
    with pytest.raises(TypeError):
        filter_by_state(invalid_transactions)


from datetime import datetime
import pytest


# Функцию берем для тестирования
def sort_by_date(data_list: list, reverse=True) -> list:
    """
    Сортирует список словарей по дате ('date'), с поддержкой обработки возможных ошибок преобразования даты.

    :param data_list: Список словарей, содержащих даты в виде строк формата ISO (например, '2023-10-07T12:34:56')
    :param reverse: Направление сортировки (True — по убыванию, False — по возрастанию), по умолчанию True.
    :return: Отсортированный список словарей.
    """
    # Удаляем записи, в которых нет ключа 'date'
    valid_data = [entry for entry in data_list if 'date' in entry]

    try:
        # Сортируем оставшиеся записи
        sorted_data = sorted(valid_data, key=lambda x: datetime.fromisoformat(x['date']), reverse=reverse)
        return sorted_data
    except ValueError as e:
        print(f"Ошибка при парсинге даты: {e}")
        return []


# Данные для тестирования
data_valid = [
    {'id': 1, 'date': '2023-10-01T12:00:00'},
    {'id': 2, 'date': '2023-10-03T15:30:00'},
    {'id': 3, 'date': '2023-10-02T10:15:00'}
]

data_missing_key = [
    {'id': 1, 'date': '2023-10-01T12:00:00'},
    {'id': 2},  # Нет ключа 'date'
    {'id': 3, 'date': '2023-10-02T10:15:00'}
]

data_wrong_format = [
    {'id': 1, 'date': '2023-10-01T12:00:00'},
    {'id': 2, 'date': 'invalid-date-format'},
    {'id': 3, 'date': '2023-10-02T10:15:00'}
]

data_empty = []


# Тест 1: Проверка правильной сортировки по умолчанию (по убыванию)
def test_sort_by_date_descending():
    result = sort_by_date(data_valid)
    expected_order = ['2023-10-03T15:30:00', '2023-10-02T10:15:00', '2023-10-01T12:00:00']
    dates = [d['date'] for d in result]
    assert dates == expected_order


# Тест 2: Проверка правильной сортировки по возрастанию
def test_sort_by_date_ascending():
    result = sort_by_date(data_valid, reverse=False)
    expected_order = ['2023-10-01T12:00:00', '2023-10-02T10:15:00', '2023-10-03T15:30:00']
    dates = [d['date'] for d in result]
    assert dates == expected_order


# Тест 3: Пропуск записей без ключа 'date'
def test_sort_skip_without_date_key():
    result = sort_by_date(data_missing_key)
    expected_order = ['2023-10-02T10:15:00', '2023-10-01T12:00:00']
    dates = [d['date'] for d in result]
    assert dates == expected_order


# Тест 4: Возвращает пустой список при отсутствии данных
def test_sort_empty_list():
    result = sort_by_date(data_empty)
    assert result == []
