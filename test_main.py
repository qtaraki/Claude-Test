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


@patch("main.yf.Ticker")
@patch("main.requests.get")
def test_current_stock_price(mock_requests_get, mock_ticker):
    mock_time_response = MagicMock()
    mock_time_response.json.return_value = {"datetime": "2025-01-15T12:00:00+00:00"}
    mock_time_response.raise_for_status.return_value = None
    mock_requests_get.return_value = mock_time_response

    mock_instance = MagicMock()
    index = pd.to_datetime(["2025-01-14", "2025-01-15"])
    mock_instance.history.return_value = pd.DataFrame({"Close": [228.50, 229.98]}, index=index)
    mock_ticker.return_value = mock_instance

    response = client.get("/stock/AAPL/now")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert data["date"] == "2025-01-15"
    assert data["close"] == 229.98


@patch("main.requests.get")
def test_time_server_failure(mock_requests_get):
    mock_requests_get.side_effect = Exception("Connection error")

    response = client.get("/stock/AAPL/now")
    assert response.status_code == 503
