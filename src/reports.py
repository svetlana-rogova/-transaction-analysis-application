import os
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from src.logger_config import logger_setting
from src.utils import decorator_write, read_excel

file = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")
transactions = read_excel(file)

logger = logger_setting("reports")


@decorator_write
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категориям за три последних месяца"""
    if date:
        end_data = ((datetime.strptime(date, "%d.%m.%Y"))).replace(hour=23, minute=59, second=59)
        start = (end_data - timedelta(days=90)).replace(hour=0, minute=0, second=0)
        logger.info("Для вычсиления трат по категории ипользуется переданное время")
    else:
        logger.info("Для вычсиления трат по категории ипользуется текущее время")
        end_data = datetime.now()
        start = (end_data - timedelta(days=90)).replace(hour=0, minute=0, second=0)

    filtered = transactions[transactions["Категория"] == category]
    filtered = filtered.copy()
    filtered["Дата операции"] = pd.to_datetime(filtered["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    wastes = filtered[filtered["Сумма операции"] < 0]
    wastes_date = wastes[(wastes["Дата операции"] >= start) & (wastes["Дата операции"] <= end_data)]
    group = wastes_date.groupby("Дата операции", as_index=False).agg({"Сумма операции": "mean", "Категория": "first"})
    logger.info("Список отформатирован и выводится в виде DataFrame с колонками: "
                "Дата операции, Сумма операции и Категория")
    return group
