from unittest.mock import MagicMock, patch

import pandas as pd
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@patch("main.yf.Ticker")
def test_valid_stock_request(mock_ticker):
    mock_instance = MagicMock()
    mock_instance.history.return_value = pd.DataFrame({"Close": [229.98]})
    mock_ticker.return_value = mock_instance

    response = client.get("/stock/AAPL", params={"date": "2025-01-15"})
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert data["date"] == "2025-01-15"
    assert data["close"] == 229.98


@patch("main.yf.Ticker")
def test_no_data_weekend(mock_ticker):
    mock_instance = MagicMock()
    mock_instance.history.return_value = pd.DataFrame()
    mock_ticker.return_value = mock_instance

    response = client.get("/stock/AAPL", params={"date": "2025-01-18"})
    assert response.status_code == 404


@patch("main.yf.Ticker")
def test_invalid_symbol(mock_ticker):
    mock_instance = MagicMock()
    mock_instance.history.return_value = pd.DataFrame()
    mock_ticker.return_value = mock_instance

    response = client.get("/stock/FAKESYMBOL", params={"date": "2025-01-15"})
    assert response.status_code == 404


def test_invalid_date_format():
    response = client.get("/stock/AAPL", params={"date": "not-a-date"})
    assert response.status_code == 422
