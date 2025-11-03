import os

from src.reports import spending_by_category
from src.services import transaction_person
from src.utils import read_excel, welcome_message
from src.views import currency_rate, filter_card, request_currencies, top_five_transactions

file = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")
transactions = read_excel(file)
dict_transactions = transactions.to_dict(orient="records")
date_and_time = "04.10.2021 12:10:06"


def generation_rusult():
    """Функция формирует итоговый словарь отчета с данными за указанную дату"""
    result = {
        "greeting": welcome_message(),
        "cards": filter_card(date_and_time),
        "top_transactions": top_five_transactions(date_and_time),
        "currency_rates": currency_rate(),
        "stock_prices": request_currencies()

    }
    return result


three_transactions = spending_by_category(transactions, "Связь", "21.10.2018")
"""Функция возвращает траты по заданной категориям за три последних месяца"""
print(three_transactions)


people_transact = transaction_person(dict_transactions)
"""Функция для вывода всех переводов физическим лицам"""
print(people_transact)
