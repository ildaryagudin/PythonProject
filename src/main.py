# main.py
import json
import csv
import openpyxl
from datetime import datetime
from typing import List, Dict
from utils import process_bank_search, process_bank_operations


def load_data(file_path):
    """Загрузка данных из файла"""
    file_extension = file_path.split('.')[-1].lower()
    try:
        if file_extension == 'json':
            with open(file_path, encoding='utf-8') as f:
                return json.load(f)
        elif file_extension == 'csv':
            with open(file_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        elif file_extension == 'xlsx':
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active
            headers = [cell.value for cell in sheet[1]]
            rows = []
            for row in sheet.iter_rows(min_row=2, values_only=True):
                rows.append(dict(zip(headers, row)))
            return rows
        else:
            raise ValueError("Неподдерживаемый формат файла")
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
        return None


def filter_by_status(data: List[Dict], status: str) -> List[Dict]:
    """Фильтрация операций по статусу."""
    return [item for item in data if item.get('state').upper() == status.upper()]


def sort_by_date(data: List[Dict], ascending: bool = True) -> List[Dict]:
    """Сортировка операций по дате."""
    sorted_data = sorted(
        data,
        key=lambda x: datetime.strptime(x.get('date'), '%Y-%m-%d'),
        reverse=not ascending
    )
    return sorted_data


def display_transactions(transactions: List[Dict]):
    """Отображение списка транзакций."""
    if not transactions:
        print("Не найдено ни одной транзакции.")
        return
    print("\nВсего банковских операций в выборке:", len(transactions))
    for idx, transaction in enumerate(transactions):
        date_str = transaction.get('date')
        amount = transaction.get('amount')
        description = transaction.get('description')

        print(f"{idx + 1}. Дата: {date_str}, Описание: {description}, Сумма: {amount}\n")


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n"
          "Выберите необходимый пункт меню:\n"
          "1. Получить информацию о транзакциях из JSON-файла\n"
          "2. Получить информацию о транзакциях из CSV-файла\n"
          "3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input("Ваш выбор: ")
        if choice == '1':
            filename = 'operations.json'
            break
        elif choice == '2':
            filename = 'transactions.csv'
            break
        elif choice == '3':
            filename = 'transactions_excel.xlsx'
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите снова.")

    data = load_data(filename)
    if not data:
        return

    valid_statuses = ['EXECUTED', 'CANCELED', 'PENDING']
    status = ''
    while status.upper() not in valid_statuses:
        status = input(f"Введите статус, по которому необходимо выполнить фильтрацию "
                       f"(доступные: {' '.join(valid_statuses)}): ").strip().upper()

    filtered_data = filter_by_status(data, status)
    print(f"\nОперации отфильтрованы по статусу '{status}'\n")

    should_sort = input("Отсортировать операции по дате? (Да/Нет): ").strip().lower()
    if should_sort.startswith('да'):
        sort_order = input("Отсортировать по возрастанию или по убыванию? (возр./убыв.): ").strip().lower()
        is_ascending = sort_order.startswith('возр.')
        filtered_data = sort_by_date(filtered_data, ascending=is_ascending)

    only_rubles = input("Вывести только рублевые транзакции? (Да/Нет): ").strip().lower()
    if only_rubles.startswith('да'):
        filtered_data = [op for op in filtered_data if op.get('currency') == 'RUB']

    word_filter = input("Отфильтровать список транзакций по определённому слову в описании? (Да/Нет): ").strip().lower()
    if word_filter.startswith('да'):
        search_word = input("Введите слово для поиска: ").strip()
        filtered_data = process_bank_search(filtered_data, search_word)

    display_transactions(filtered_data)


if __name__ == "__main__":
    main()