import json
import pandas as pd
from typing import List, Dict
import logging
from datetime import datetime
import os

# Настройка логирования
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)  # Создаем папку logs, если её нет

log_filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_app.log"
log_filepath = os.path.join(LOG_DIR, log_filename)

logging.basicConfig(
    filename=log_filepath,
    level=logging.DEBUG,
    format="%(asctime)s - %(module)s - %(levelname)s - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode="w"  # Записываем новый файл журнала каждый раз при запуске
)

logger = logging.getLogger(__name__)


def load_transactions(file_path: str, file_type: str = None) -> List[Dict]:
    """
    Загружает финансовые операции из файла соответствующего формата.

    :param file_path: Путь к файлу с транзакциями.
    :param file_type: Тип файла ('json', 'csv', 'xlsx'). Если не указан, определяется автоматически.
    :return: Список транзакций или пустой список в случае ошибок.
    """
    if file_type is None:
        _, ext = os.path.splitext(file_path)
        file_type = ext.lstrip('.').lower()

    try:
        if file_type == 'json':
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            if isinstance(data, list):
                logger.info(f'Успешно загрузил {len(data)} транзакций из файла {file_path}')
                return data
            else:
                logger.warning(f'Файл {file_path} содержит некорректный формат списка транзакций.')
                return []

        elif file_type == 'csv':
            df = pd.read_csv(file_path)
            data = df.to_dict(orient='records')
            logger.info(f'Успешно загрузил {len(data)} транзакций из файла {file_path}')
            return data

        elif file_type == 'xlsx':
            df = pd.read_excel(file_path)
            data = df.to_dict(orient='records')
            logger.info(f'Успешно загрузил {len(data)} транзакций из файла {file_path}')
            return data

        else:
            logger.error(f'Невозможно обработать файл {file_path}: неизвестный формат файла.')
            return []

    except Exception as e:
        logger.error(f'Ошибка при обработке файла {file_path}: {str(e)}')
        return []