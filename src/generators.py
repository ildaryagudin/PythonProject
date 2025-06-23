def filter_by_currency(transactions, currency_code):
    return (
        transaction
        for transaction in transactions
        if transaction['operationAmount']['currency']['code'] == currency_code
    )


def transaction_descriptions(transactions):
    """
    Генерирует последовательность описаний транзакций.
    :param transactions: список словарей с информацией о транзакциях
    :return: генератор строк с описанием каждой транзакции
    """
    return (transaction["description"] for transaction in transactions)


def card_number_generator(start=1, end=9999999999999999):
    """
    Генератор, выдающий номера банковских карт в формате XXXX XXXX XXXX XXXX.
    start: Начальная точка диапазона (по умолчанию 1)
    end: Конечная точка диапазона (по умолчанию 9999999999999999)
    """
    for number in range(start, end + 1):
        formatted_card_number = "{:016d}".format(number)  # Добавляем ведущие нули
        yield f"{formatted_card_number[:4]} {formatted_card_number[4:8]} {formatted_card_number[8:12]} {formatted_card_number[12:]}"