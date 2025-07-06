from src.decorators import log  # Импортируем ваш декоратор
import os
import tempfile
import pytest


@pytest.fixture
def temp_log_file():
    """Фикстура для временного файла"""
    fd, path = tempfile.mkstemp(suffix='.txt')
    yield path
    os.close(fd)
    os.unlink(path)


# Тест успешного выполнения функции
def test_successful_execution(capsys):
    @log()
    def successful_function():
        return "OK"

    successful_function()
    captured = capsys.readouterr()  # Перехватываем вывод в stdout
    assert "successful_function ok" in captured.out


# Тест обработки ошибки
def test_error_handling(temp_log_file):
    @log(filename=temp_log_file)
    def failing_function():
        raise ValueError("Test Error")

    failing_function()
    with open(temp_log_file, 'r') as file:
        content = file.read()
        assert "failing_function error:" in content
        assert "ValueError" in content


# Тест функциональности логирования в файл
def test_logging_to_file(temp_log_file):
    @log(filename=temp_log_file)
    def function_with_result():
        return "Result OK"

    function_with_result()
    with open(temp_log_file, 'r') as file:
        content = file.read()
        assert "function_with_result ok" in content


# Тест с разными типами аргументов
def test_decorator_with_args_and_kwargs(capsys):
    @log()
    def decorated_function(x, y, z=3):
        return x * y * z

    decorated_function(2, 3, z=4)
    captured = capsys.readouterr()
    assert "decorated_function ok" in captured.out


# Тест на отсутствие файла при неудаче
def test_no_file_on_console_output():
    @log()
    def console_only_function():
        pass

    console_only_function()
    # Мы ожидаем, что ничего не было создано в файловой системе
    for root, dirs, files in os.walk(os.curdir):
        for file in files:
            assert "console.log" not in file