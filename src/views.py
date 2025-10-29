import os
from datetime import datetime
from src.utils import read_excel
import pandas as pd


date_and_time = "04.10.2021"
file = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")
df = read_excel(file)


def get_date_interval(date_and_time):
    """Функция рассчитывает нужный интервал, получая дату"""
    end = datetime.strptime(date_and_time, "%d.%m.%Y")
    end = end.replace(hour=23, minute=59, second=59)
    start = end.replace(day=1, hour=0, minute=0, second=0)
    dates = start, end
    return dates


def filter_date(date_and_time):
    """Фильтруем наши данные по нужному интервалу дат"""
    start, end = get_date_interval(date_and_time)
    filter = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    filtered = df[(filter >= start) & (filter <= end)]
    return filtered

