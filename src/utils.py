import pandas as pd
import os
import json


file = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")
def read_excel(file):
    """Функция для преобразования excel файла в список словарей"""
    try:
        df = pd.read_excel(file)
        return df
    except FileNotFoundError:
        return "Файл не найден"


def open_user_setting():
    """Открываем json файл и заносим данные из него в отдельные переменные, которые будут содержать валюты и фонды"""
    file = os.path.join(os.path.dirname(__file__), "..", "user_settings.json")
    with open(file, "r", encoding="utf-8") as f:
        user_settings = json.load(f)
        currencies = user_settings["user_currencies"]
        stocks = user_settings["user_stocks"]
    settings = currencies, stocks
    return settings
