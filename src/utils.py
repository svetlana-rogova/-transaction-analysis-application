import pandas as pd
import os
from datetime import datetime
import json


file = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")
def read_excel(file):
    """Функция для преобразования excel файла в список словарей"""
    try:
        df = pd.read_excel(file)
        return df
    except FileNotFoundError:
        return "Файл не найден"


def welcome_message():
    """Функция возвращает приветственное сообщение в зависимости от времени суток"""
    today = datetime.now()
    time_now = today.strftime("%H")
    if  int(time_now) in range(6,12):
        return "Доброе утро"
    elif int(time_now) in range(12,18):
        return "Добрый день"
    elif int(time_now) in range(18,24):
        return "Добрый вечер"
    elif int(time_now) in range(0,6):
        return  "Доброй ночи"


def open_user_setting():
    """Открываем json файл и заносим данные из него в отдельные переменные, которые будут содержать валюты и фонды"""
    file = os.path.join(os.path.dirname(__file__), "..", "user_settings.json")
    with open(file, "r", encoding="utf-8") as f:
        user_settings = json.load(f)
        currencies = user_settings["user_currencies"]
        stocks = user_settings["user_stocks"]
    settings = currencies, stocks
    return settings
