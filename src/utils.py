import json
from typing import List, Dict
import logging
from datetime import datetime
import os


# Настраиваем логирование
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)  # создаем каталог logs, если его нет

log_filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_app.log"
log_filepath = os.path.join(LOG_DIR, log_filename)

logging.basicConfig(
    filename=log_filepath,
    level=logging.DEBUG,
    format="%(asctime)s - %(module)s - %(levelname)s - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode="w"  # Перезапись файла при каждом новом запуске программы
)

logger = logging.getLogger(__name__)  # получаем объект логгера для текущего модуля


def load_transactions(file_path: str) -> List[Dict]:
    """
    Функция загружает транзакции из указанного JSON-файла.
    Возвращает список транзакций или пустой список в случае ошибки.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if isinstance(data, list):
            logger.info(f'Successfully loaded {len(data)} transactions from {file_path}.')
            return data
        else:
            logger.warning(f'The content in {file_path} is not a valid list of transactions.')
            return []

    except FileNotFoundError:
        logger.error(f'File {file_path} was not found.')
        return []
    except json.JSONDecodeError:
        logger.error(f'{file_path} contains invalid JSON format.')
        return []

# Пример использования
transactions = load_transactions('example.json')
for transaction in transactions:
    print(transaction)