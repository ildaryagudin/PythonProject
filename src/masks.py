def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску"""
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError("Неверный формат номера карты")

    masked_part = '****' * 2  # генерируем две группы звездочек
    return f"{card_number[:4]} {card_number[4:6]}** {masked_part} {card_number[-4:]}"


def get_mask_account(card_account: str) -> str:
    """Функция получает номер счета и выводит ** с последними 4мя цифрами"""
    card_account = card_account.replace(" ", "")
    print(len(card_account))
    if len(card_account) != 20 and not card_account.isdigit():
        return "Неверное количество или значение цифр"
    last_part = str(card_account[-4:])
    return f"**{last_part}"
