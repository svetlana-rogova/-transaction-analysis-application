import json
import os
import re

from src.logger_config import logger_setting
from src.utils import read_excel

logger = logger_setting("services")

file = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")
transactions = read_excel(file)
dict_transactions = transactions.to_dict(orient="records")

file_people = os.path.join(os.path.dirname(__file__), "..", "data", "file_people.json")


def transaction_person(dict_transactions):
    """Функция для вывода всех переводов физическим лицам"""
    filtered = [transact for transact in dict_transactions if transact["Категория"] == "Переводы"]
    pattern = r"^[А-ЯЁA-Z][а-яёa-z]+\s[А-ЯЁA-Z]\.$"
    filtered_people = [transact for transact in filtered if re.match(pattern, transact["Описание"])]
    with open(os.path.join(os.path.dirname(__file__), "..", "data", "file_people.json"), "w", encoding="utf-8") as f:
        json.dump(filtered_people, f, ensure_ascii=False, indent=4)
        logger.info("Файл 'file_people.json' создан и в него записаны данные о переводах физическим лицам")
    return filtered_people
