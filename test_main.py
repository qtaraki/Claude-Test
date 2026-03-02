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
    mock_time_response.json.return_value = {"dateTime": "2025-01-15T12:00:00"}
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


@patch("main.requests.get")
def test_current_crypto_price(mock_requests_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"bitcoin": {"usd": 66875}}
    mock_requests_get.return_value = mock_response

    response = client.get("/crypto/bitcoin/now")
    assert response.status_code == 200
    data = response.json()
    assert data["coin"] == "bitcoin"
    assert data["price"] == 66875.0


@patch("main.requests.get")
def test_current_crypto_invalid_coin(mock_requests_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {}
    mock_requests_get.return_value = mock_response

    response = client.get("/crypto/fakecoin/now")
    assert response.status_code == 404


@patch("main.requests.get")
def test_historical_crypto_price(mock_requests_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "market_data": {"current_price": {"usd": 97007.78}}
    }
    mock_requests_get.return_value = mock_response

    response = client.get("/crypto/bitcoin", params={"date": "2026-01-15"})
    assert response.status_code == 200
    data = response.json()
    assert data["coin"] == "bitcoin"
    assert data["date"] == "2026-01-15"
    assert data["price"] == 97007.78


@patch("main.requests.get")
def test_historical_crypto_invalid_coin(mock_requests_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_requests_get.return_value = mock_response

    response = client.get("/crypto/fakecoin", params={"date": "2026-01-15"})
    assert response.status_code == 404
