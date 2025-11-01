from src.utils import read_excel, welcome_message, open_user_setting
from unittest.mock import patch, mock_open
from freezegun import freeze_time
import json


@patch("pandas.read_excel")
def test_read_excel(mock_read_excel):
    mock_read_excel.return_value = " "
    assert read_excel("file") == " "


@freeze_time("2023-03-12 12:30:00")
def test_welcome_message():
    assert welcome_message() == "Добрый день"


def test_open_user_setting():
    mock_data = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN"]
    }
    m = mock_open(read_data=json.dumps(mock_data))
    with patch("builtins.open", m):
        result = open_user_setting()

    assert result == (["USD", "EUR"], ["AAPL", "AMZN"])

