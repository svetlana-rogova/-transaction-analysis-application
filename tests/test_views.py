import datetime
from unittest.mock import patch

import pytest

from src.views import (currency_rate, filter_card, filter_date, get_date_interval, request_currencies,
                       top_five_transactions)


@pytest.mark.parametrize(
    "time_and_date, expected_response",
    [
        ("11.03.2024", (datetime.datetime(2024, 3, 1, 0, 0), datetime.datetime(2024, 3, 11, 23, 59, 59))),
        ("17.09.2025 11:11:45", (datetime.datetime(2025, 9, 1, 0, 0), datetime.datetime(2025, 9, 17, 23, 59, 59))),
    ],
)
def test_get_date_interval(time_and_date, expected_response):
    assert get_date_interval(time_and_date) == expected_response


def test_filter_date(sample_transactions):
    with patch("src.views.df", sample_transactions):
        assert len(filter_date("02.01.2023 12:30:00")) == 2
        assert (filter_date("02.01.2023 12:30:00")).iloc[1]["Категория"] == "Переводы"


def test_filter_card(sample_transactions):
    with patch("src.views.filter_date", return_value=sample_transactions):
        assert filter_card("01.01.2023 12:30:00") == [{"cashback": 6.0, "last_digits": "*1111", "total_spent": -600.0}]


def test_top_five_transactions(sample_transactions):
    with patch("src.views.filter_date", return_value=sample_transactions):
        assert top_five_transactions("01.01.2023 12:30:00")[0] == {
            "amount": 300,
            "category": "Аптека",
            "date": "12.03.2023 11:30:00",
            "description": "Парикмахерская",
        }


@patch("requests.get")
def test_request_currencies(mock_get):
    with patch("src.views.stocks", ["AAPL", "AMZN"]):
        mock_get.return_value.json.return_value = {"Global Quote": {"05. price": "123"}}
        result = request_currencies()
    assert result == [{"currency": "AAPL", "rate": "123"}, {"currency": "AMZN", "rate": "123"}]


@patch("requests.get")
def test_currency_rate(mock_get):
    with patch("src.views.currencies", ["USD"]):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"source": "EUR", "quotes": {"EURRUB": 93.250219}}
        result = currency_rate()
    assert result == [{"currency": "USD", "rate": 93.250219}]
