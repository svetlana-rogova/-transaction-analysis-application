import json
import os

from src.utils import read_excel

file = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")
transactions = read_excel(file)

file_people = os.path.join(os.path.dirname(__file__), "..", "data", "file_people.json")


def transaction_person(transactions):
    """Функция для вывода всех переводов физическим лицам"""
    filtered = transactions[transactions["Категория"] == "Переводы"]
    filter_transactions = filtered[filtered["Описание"].str.match(r"^[А-ЯЁA-Z][а-яёa-z]+\s[А-ЯЁA-Z]\.$", na=False)]
    filter_dict = filter_transactions.to_dict(orient="records")
    with open(os.path.join(os.path.dirname(__file__), "..", "data", "file_people.json"), "w", encoding="utf-8") as f:
        json.dump(filter_dict, f, ensure_ascii=False, indent=4)


print(transaction_person(transactions))
