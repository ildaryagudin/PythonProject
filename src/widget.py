from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_or_account_number: str) -> str:
    """
    Функция обработки информацию
    о картах и счетах
    """
    if "Счет" in card_or_account_number:
        number = card_or_account_number.replace("Счет", "").strip()
        return "Счет " + get_mask_account(number)
    else:
        number = get_mask_card_number(card_or_account_number[-16:])
        updated_card_number = " ".join(card_or_account_number.split()[:-1]) + " " + number
        return updated_card_number

print(mask_account_card('Maestro 1596837868705199'))
import re


def get_date(date_string):
    # Регулярное выражение извлекает числа года, месяца и дня из строки
    match = re.match(r'(\d{4})-(\d{2})-(\d{2})', date_string)

    if match:
        year, month, day = match.groups()

        # Собираем дату в нужном формате
        formatted_date = f"{day}.{month}.{year}"
        return formatted_date
    else:
        raise ValueError("Неверный формат даты")


