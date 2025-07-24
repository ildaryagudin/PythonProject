import pytest

from src.masks import get_mask_card_number  # Импортируем вашу функцию из модуля


# Базовый тест для правильной обработки карт длиной ровно 16 знаков
def test_valid_16_digit_card():
    result = get_mask_card_number('1234567890123456')
    assert result == '1234 56** ******** 3456'

# Проверка короткого ввода — менее 16 цифр должно вызвать ValueError
def test_invalid_length_shorter_than_16_digits():
    with pytest.raises(ValueError):
        get_mask_card_number('123456789012345')  # 15 цифр

# Проверка длинного ввода — больше 16 цифр тоже вызывает ValueError
def test_invalid_length_longer_than_16_digits():
    with pytest.raises(ValueError):
        get_mask_card_number('12345678901234567')  # 17 цифр

# Тестирование неверного формата вводимых данных (буквы/нечисла)
def test_non_numeric_input():
    with pytest.raises(ValueError):
        get_mask_card_number('1234567890abcdef')

# Пустой ввод должен вызывать ошибку
def test_empty_string():
    with pytest.raises(ValueError):
        get_mask_card_number('')

# Строка, состоящая только из пробелов, должна привести к ошибке
def test_only_spaces():
    with pytest.raises(ValueError):
        get_mask_card_number('     ')

# Обработка строки с числами, окаймлёнными пробелами
def test_correctly_handles_whitespace_around():
    result = get_mask_card_number('   1234567890123456   ')
    assert result.strip() == '1234 56** ******** 3456'



from src.masks import get_mask_account  # импорт вашего модуля с функцией

# Тестовая функция проверки правильности вывода для верного формата счёта
def test_get_mask_account_valid():
    account = "12345678901234567890"
    expected_result = "**7890"
    actual_result = get_mask_account(account)
    assert actual_result == expected_result, f"Ошибка! Ожидалось {expected_result}, получено {actual_result}"

# Тест случая неправильного количества цифр
@pytest.mark.parametrize("account, error_message", [
    ("1234567890123456789", "Неверное количество или значение цифр"),  # 19 цифр
    ("123456789012345678901", "Неверное количество или значение цифр")  # 21 цифра
])
def test_get_mask_account_incorrect_length(account, error_message):
    result = get_mask_account(account)
    assert result == error_message, f"Ошибка! Ожидалось сообщение '{error_message}', получилось '{result}'"

# Тест недопустимого формата (символы вместо цифр)
def test_get_mask_account_invalid_format():
    account = "abcde123456789012345"
    expected_error = "Неверное количество или значение цифр"
    result = get_mask_account(account)
    assert result == expected_error, f"Ошибка! Ожидалось сообщение '{expected_error}', получилось '{result}'"

# Тест пустой строки
def test_get_mask_account_empty_string():
    account = ""
    expected_error = "Неверное количество или значение цифр"
    result = get_mask_account(account)
    assert result == expected_error, f"Ошибка! Ожидалось сообщение '{expected_error}', получилось '{result}'"

# Тест строки с лишними пробелами вокруг
def test_get_mask_account_with_whitespaces():
    account = "  12345678901234567890  "
    expected_result = "**7890"
    result = get_mask_account(account)
    assert result == expected_result, f"Ошибка! Ожидалось {expected_result}, получено {result}"