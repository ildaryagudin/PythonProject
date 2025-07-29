import pytest
from src.main import (
    process_bank_search,
    process_bank_operations,
    load_data,
    filter_by_status,
    sort_by_date
)

@pytest.fixture
def sample_data():
    return [
        {"id": 1, "description": "Оплата кафе", "amount": 500},
        {"id": 2, "description": "Перевод другу", "amount": 1000},
        {"id": 3, "description": "Покупка продуктов", "amount": 2000},
        {"id": 4, "description": "Абонемент спортзал", "amount": 1500},
        {"id": 5, "description": "Оплата такси", "amount": 700},
    ]

# Тестирование функции поиска по операции
def test_process_bank_search(sample_data):
    results = process_bank_search(sample_data, "оплата")
    assert len(results) == 2
    assert all("оплата" in op["description"].lower() for op in results)

# Тестирование подсчета операций по категориям
def test_process_bank_operations(sample_data):
    categories = ["кафе", "продукты"]
    expected_result = {"кафе": 1, "продукты": 1}
    actual_result = process_bank_operations(sample_data, categories)
    assert actual_result == expected_result

# Проверяем загрузку JSON-данных
def test_load_json(tmpdir):
    p = tmpdir.join("sample.json")
    p.write('{"transactions": [{"id": 1, "description": "Тестовая операция"}]}')
    loaded_data = load_data(str(p))
    assert isinstance(loaded_data, list)
    assert len(loaded_data) > 0

# Загружаем CSV-данные
def test_load_csv(tmpdir):
    p = tmpdir.join("sample.csv")
    p.write_text("id,description\\n1,Операция 1\\n2,Операция 2", encoding="utf-8")
    loaded_data = load_data(str(p))
    assert isinstance(loaded_data, list)
    assert len(loaded_data) == 2

# Тестируем фильтрование по статусу
def test_filter_by_status(sample_data):
    filtered_data = filter_by_status([{"state": "Выполнено"}, {"state": "Отменено"}], "выполнено")
    assert len(filtered_data) == 1
    assert filtered_data[0]["state"] == "Выполнено"

# Тестируем сортировку по дате
def test_sort_by_date():
    operations = [
        {"date": "2023-01-01"},
        {"date": "2023-01-02"}
    ]
    sorted_ops = sort_by_date(operations)
    assert sorted_ops[0]["date"] == "2023-01-01"
    reversed_sorted_ops = sort_by_date(operations, ascending=False)
    assert reversed_sorted_ops[0]["date"] == "2023-01-02"

if __name__ == "__main__":
    pytest.main()