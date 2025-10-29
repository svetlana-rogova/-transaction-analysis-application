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


def filter_card(date_and_time):
    """Функция фильтрует данные по картам и выводит список словарей с номерами карт и данными по ним"""
    fd = filter_date(date_and_time).copy()
    fd["Номер карты"] = fd["Номер карты"].replace(r'^\s*$', float("nan"))
    cards = set(fd["Номер карты"])
    cards_data = []
    for card in cards:
        if pd.isna(card):
            card_df = fd[fd["Номер карты"].isna()]
        else:
            card_df = fd[fd["Номер карты"] == card]
        amount_expenses = card_df[card_df["Сумма операции"]<0]["Сумма операции"].sum()
        total_spent = round(float(amount_expenses),2)
        cashback = (round(total_spent/100, 2))*-1

        cards_data.append({
            "last_digits": card,
            "total_spent": total_spent,
            "cashback": cashback
        })
    return cards_data


def top_five_transactions(date_and_time):
    fd = filter_date(date_and_time)
    transactions_df = fd.groupby(["Категория", "Описание", "Дата платежа"])["Сумма операции с округлением"].sum()
    sort_transactions_df = transactions_df.sort_values(ascending=False)
    top_five = sort_transactions_df.head().reset_index()
    dict_top_five = top_five.to_dict(orient='records')
    conclusion = []
    for date in dict_top_five:
        conclusion.append({
            "date": date['Дата платежа'],
            "amount": date['Сумма операции с округлением'],
            "category": date['Категория'],
            "description": date['Описание']
        })
    return conclusion

