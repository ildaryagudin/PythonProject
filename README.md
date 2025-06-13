# PythonProject
PythonProject — банковский виджет, предназначенный для обработки и фильтрации финансовых транзакций клиентов банка.

---

## Описание

Данный проект представляет собой библиотеку для удобного анализа банковской активности пользователей. Основной функциональностью является фильтрация транзакций по статусу операции (state), что позволяет легко выделять выполненные, отменённые или ожидающие подтверждения платежи.

---

## Установка

Чтобы установить проект локально, выполните следующие шаги:

git clone https://github.com/ildaryagudin/PythonProject.git
cd PythonProject
pip install -r requirements.txt
---

## Использование

Основной модуль — processing.py, содержащий ключевую функцию filter_by_state(), которая фильтрует банковские операции по состоянию платежа.

Аргументы функции:
- operations_list: список словарей, содержащих данные о каждой транзакции.
- state_value (опциональный аргумент): строка состояния («EXECUTED», «CANCELED» и др.). По умолчанию установлен в «EXECUTED».

Возвращаемое значение:
Новый список словарей, включающий только транзакции, соответствующие заданному состоянию.

## Пример использования:

from processing import filter_by_state

operations = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"}
]

filtered_operations_executed = filter_by_state(operations)
print(filtered_operations_executed)

filtered_operations_canceled = filter_by_state(operations, "CANCELED")
print(filtered_operations_canceled)
Результат выполнения приведённого примера:

[
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
]

[
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
]