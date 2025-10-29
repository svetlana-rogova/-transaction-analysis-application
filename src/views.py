import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

from src.utils import open_user_setting, read_excel, welcome_message


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
        amount_expenses = card_df[card_df["Сумма операции"] < 0]["Сумма операции"].sum()
        total_spent = round(float(amount_expenses), 2)
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


"""Читаем наш API ключ для доступа к данным на стороннем сервере"""
load_dotenv()
API_KEY = os.getenv("API_KEY")
headers = {"apikey": API_KEY}
API_KEY_TWO = os.getenv("API_KEY_TWO")
headers_two = {"apikey": API_KEY_TWO}


currencies, stocks = open_user_setting()


def request_currencies():
    """Получаем ценs акций из пользовательского списка"""
    company_rate = []
    for company in stocks:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={company}&apikey=headers'
        r = requests.get(url)
        data = r.json()
        company_rate.append({
                             "currency": company,
                            "rate": data["Global Quote"]["05. price"]
                            })
    return company_rate


def currency_rate():
    """Получаем курсы валют из пользовательского списка"""
    list_currency = []
    for currency in currencies:
        url = f"https://api.apilayer.com/currency_data/live?source={currency}&currencies=RUB"
        response = requests.get(url, headers=headers_two)
        if response.status_code == 200:
            data = response.json()
            list_currency.append({
                "currency": currency,
                "rate": list(data['quotes'].values())[0]
            })
        else:
            return f"Ошибка {response.status_code}"
    return list_currency


result = {
    "greeting": welcome_message(),
    "cards": filter_card(date_and_time),
    "top_transactions": top_five_transactions(date_and_time),
    "currency_rates": currency_rate(),
    "stock_prices": request_currencies()

}
print(result)
