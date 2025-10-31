import json
import logging
import os
from datetime import datetime

import pandas as pd

log_path = os.path.join(os.path.dirname(__file__), "../logs/utils.log")
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(log_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(levelname)s %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


file = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")


def read_excel(file):
    """Функция для преобразования excel файла в список словарей"""
    try:
        df = pd.read_excel(file)
        logger.info("Файл прочитан")
        return df
    except FileNotFoundError:
        logger.error("Файл не найден")
        return "Файл не найден"


def welcome_message():
    """Функция возвращает приветственное сообщение в зависимости от времени суток"""
    today = datetime.now()
    time_now = today.strftime("%H")
    if int(time_now) in range(6, 12):
        logger.info("Программа работает, вывод: 'Доброе утро'")
        return "Доброе утро"
    elif int(time_now) in range(12, 18):
        logger.info("Программа работает, вывод: 'Добрый день'")
        return "Добрый день"
    elif int(time_now) in range(18, 24):
        logger.info("Программа работает, вывод: 'Добрый вечер'")
        return "Добрый вечер"
    elif int(time_now) in range(0, 6):
        logger.info("Программа работает, вывод: 'Доброй ночи'")
        return "Доброй ночи"


def open_user_setting():
    """Открываем json файл и заносим данные из него в отдельные переменные, которые будут содержать валюты и фонды"""
    file = os.path.join(os.path.dirname(__file__), "..", "user_settings.json")
    try:
        with open(file, "r", encoding="utf-8") as f:
            user_settings = json.load(f)
            currencies = user_settings["user_currencies"]
            stocks = user_settings["user_stocks"]
        settings = currencies, stocks
        logger.info("Файл успешно прочитан, переменные успешно выведены")
        return settings
    except FileNotFoundError:
        logger.error("Файл не найден")
        return "Файл не найден"


def decorator_write(func):
    def wrapper(*args, **kwargs):
        place = os.path.join(os.path.dirname(__file__), "..", "data")
        filename = f"{func.__name__}.json"
        file_inf = os.path.join(place, filename)
        write_file = func(*args, **kwargs)
        write_file["Дата операции"] = write_file["Дата операции"].dt.strftime("%d.%m.%Y %H:%M:%S")
        write_file = write_file.to_json(force_ascii=False, orient="records", indent=4)
        with open(file_inf, "w", encoding="utf-8") as f:
            f.write(write_file)
    return wrapper
