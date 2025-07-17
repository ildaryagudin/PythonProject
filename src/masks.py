import logging
from datetime import datetime

# Настройка логгера
log_dir = './logs'
log_file_name = f'{datetime.now().strftime("%Y-%m-%d")}.log'

# Создаем директорию logs, если её ещё нет
import os

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(f'{log_dir}/{log_file_name}')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску."""
    try:
        card_number = card_number.strip()

        if len(card_number) != 16 or not card_number.isdigit():
            logger.error("Номер карты некорректен.")
            raise ValueError("Неверный формат номера карты")

        masked_part = '****' * 2  # генерируем две группы звездочек
        result = f"{card_number[:4]} {card_number[4:6]}** {masked_part} {card_number[-4:]}"
        logger.info("Маска номера карты успешно создана.")
        return result
    except Exception as e:
        logger.exception("Ошибка при маскировании номера карты.", exc_info=True)
        raise e


def get_mask_account(card_account: str) -> str:
    """Функция получает номер счёта и выводит ** с последними четырьмя цифрами."""
    try:
        card_account = card_account.replace(" ", "")
        if len(card_account) != 20 or not card_account.isdigit():
            logger.warning("Номер счёта имеет неверный формат.")
            return "Неверное количество или значение цифр"
        last_part = str(card_account[-4:])
        result = f"**{last_part}"
        logger.info("Маска номера счёта успешно создана.")
        return result
    except Exception as e:
        logger.exception("Ошибка при маскировании номера счёта.", exc_info=True)
        raise e