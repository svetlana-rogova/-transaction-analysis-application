import json
from unittest.mock import mock_open, patch

from src.reports import spending_by_category


def tests_spending_by_category(sample_transactions):
    m = mock_open()
    with patch("src.utils.open", m):
        data_transact = spending_by_category(sample_transactions, "Супермаркеты", "01.01.2023")
        row = json.loads(data_transact)
    assert row[0] == {
        "Дата операции": "01.01.2023 10:00:00",
        "Сумма платежа": -100.0,
        "Категория": "Супермаркеты"
    }
