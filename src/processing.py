def filter_by_state(transactions_list, state='EXECUTED'):
    """
    Фильтрует список транзакций по значению поля 'state'.

    :param transactions_list: Список словарей-транзакций.
    :param state: Целевое значение поля 'state' (по умолчанию 'EXECUTED').
    :return: Список словарей, у которых поле 'state' соответствует указанному значению.
    """
    return [trans for trans in transactions_list if trans['state'] == state]


from datetime import datetime


def sort_by_date(data_list: list, reverse=True) -> list:
    """
    Сортирует список словарей по дате ('date'), с поддержкой обработки возможных ошибок преобразования даты.

    :param data_list: Список словарей, содержащих даты в виде строк формата ISO (например, '2023-10-07T12:34:56')
    :param reverse: Направление сортировки (True — по убыванию, False — по возрастанию), по умолчанию True.
    :return: Отсортированный список словарей.
    """
    # Сначала удалим записи, в которых нет ключа 'date'
    valid_data = [entry for entry in data_list if 'date' in entry]

    try:
        # Теперь сортируем оставшиеся записи
        sorted_data = sorted(valid_data, key=lambda x: datetime.fromisoformat(x['date']), reverse=reverse)
        return sorted_data
    except ValueError as e:
        print(f"Ошибка при парсинге даты: {e}")
        return []