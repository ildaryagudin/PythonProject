import pytest
from src.generators import filter_by_currency
from src.generators import transaction_descriptions
from src.generators import card_number_generator


@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 1,
            "operationAmount": {"amount": "100", "currency": {"code": "RUB"}},
            "description": "Операция №1"
        },
        {
            "id": 2,
            "operationAmount": {"amount": "200", "currency": {"code": "USD"}},
            "description": "Операция №2"
        },
        {
            "id": 3,
            "operationAmount": {"amount": "300", "currency": {"code": "EUR"}},
            "description": "Операция №3"
        },
        {
            "id": 4,
            "operationAmount": {"amount": "400", "currency": {"code": "USD"}},
            "description": "Операция №4"
        }
    ]

def test_filter_by_currency_with_valid_currency(sample_transactions):
    usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
    assert len(usd_transactions) == 2
    assert all(transaction['operationAmount']['currency']['code'] == 'USD' for transaction in usd_transactions)

def test_filter_by_currency_no_matching_currency(sample_transactions):
    jpy_transactions = list(filter_by_currency(sample_transactions, "JPY"))
    assert not jpy_transactions

def test_filter_by_currency_empty_list():
    empty_transactions = []
    result = list(filter_by_currency(empty_transactions, "USD"))
    assert not result



def test_transaction_descriptions_valid_data(sample_transactions):
    expected_descriptions = ["Операция №1", "Операция №2", "Операция №3", "Операция №4"]
    actual_descriptions = list(transaction_descriptions(sample_transactions))
    assert actual_descriptions == expected_descriptions

def test_transaction_descriptions_empty_list():
    empty_transactions = []
    result = list(transaction_descriptions(empty_transactions))
    assert not result


def test_card_number_generator():
    numbers = list(card_number_generator(1, 5))
    expected_numbers = ['0000 0000 0000 0001', '0000 0000 0000 0002', '0000 0000 0000 0003', '0000 0000 0000 0004', '0000 0000 0000 0005']
    assert numbers == expected_numbers

def test_card_number_generator_edge_cases():
    edge_case_1 = next(card_number_generator(1, 1))  # Только одна карта
    assert edge_case_1 == '0000 0000 0000 0001'

    edge_case_max = next(card_number_generator(9999999999999999, 9999999999999999))  # Максимально возможная карта
    assert edge_case_max == '9999 9999 9999 9999'