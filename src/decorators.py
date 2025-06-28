import functools
import logging

# Настройка формата вывода логов
LOG_FORMAT = "%(asctime)s %(levelname)-8s [%(name)s]: %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
logger = logging.getLogger("FunctionLogger")


def log(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Запись имени функции и старт выполнения
                message = f"{func.__name__}"

                if filename is not None:
                    handler = logging.FileHandler(filename)
                    logger.addHandler(handler)

                result = func(*args, **kwargs)

                # Добавляем сообщение о результате
                message += " ok"

            except Exception as e:
                # Логируем ошибку вместе с параметрами
                message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"

            finally:
                # Выполняем запись в файл или вывод в консоль
                if filename is not None:
                    with open(filename, 'a') as file:
                        print(message, file=file)
                else:
                    print(message)

                # Удаляем обработчик файлового логирования, если использовался
                if filename is not None:
                    logger.removeHandler(handler)

        return wrapper

    return decorator