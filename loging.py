import os
import sys
import logging


def log_func() -> None:
    """
    Настройки логгирования
    :return:
    """
    # Удаление всех обработчиков из логгера по умолчанию
    logging.root.handlers = []

    # Получение текущего рабочего каталога
    base_dir = os.getcwd()

    # Добавление обработчика для файла debug.log
    debug_handler = logging.FileHandler(f'{base_dir}/debug.log')
    debug_handler.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s | %(module)s.%(funcName)s'
    ))
    debug_handler.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(debug_handler)

    # Добавление обработчика для файла error.log
    error_handler = logging.FileHandler(f'{base_dir}/error.log')
    error_handler.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s | %(module)s.%(funcName)s'
    ))
    error_handler.setLevel(logging.ERROR)
    logging.getLogger().addHandler(error_handler)

    # Добавление обработчика для вывода в stdout
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter(
        '<green>%(asctime)s</green> | <level>%(levelname)s</level> | %(message)s | %(module)s:%(funcName)s'
    ))
    stream_handler.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(stream_handler)

    # Установка уровня  логирования для всего логгера
    logging.getLogger().setLevel(logging.DEBUG)
