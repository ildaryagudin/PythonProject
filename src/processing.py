def filter_by_state(data_list: list, state='EXECUTED') -> list:
    """
    Фильтрует список словарей по значению ключа 'state'.

    :param data_list: Список словарей, каждый словарь содержит ключи и значения.
    :param state: Значение фильтра по ключу 'state'. По умолчанию — 'EXECUTED'.
    :return: Новый список словарей, соответствующий фильтру.
    """
    return [item for item in data_list if item.get('state') == state]


from datetime import datetime


def sort_by_date(data_list: list, reverse=True) -> list:
    """
    Сортирует список словарей по дате ('date'), с поддержкой обработки возможных ошибок преобразования даты.

    :param data_list: Список словарей, содержащих даты в виде строк формата ISO (например, '2023-10-07T12:34:56')
    :param reverse: Направление сортировки (True — по убыванию, False — по возрастанию), по умолчанию True.
    :return: Отсортированный список словарей.
    """
    try:
        # Используем лямбду-функцию внутри sorted()
        sorted_data = sorted(
            data_list,
            key=lambda x: datetime.fromisoformat(x['date']),
            reverse=reverse
        )
        return sorted_data
    except ValueError as e:
        print(f"Ошибка при парсинге даты: {e}")
        return []