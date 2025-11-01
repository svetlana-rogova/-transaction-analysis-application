from unittest.mock import mock_open, patch

from src.services import transaction_person


def test_transaction_person(data_people):
    m = mock_open()
    with patch("src.services.open", m):
        answer = transaction_person(data_people)
    assert answer == [{
        "Дата операции": "05.09.2020 13:51:12",
        "Номер карты": None,
        "Статус": "OK",
        "Сумма операции": -88.0,
        "Валюта операции": "RUB",
        "Сумма платежа": -88.0,
        "Валюта платежа": "RUB",
        "Категория": "Переводы",
        "Описание": "Валерий А.",
    }]
