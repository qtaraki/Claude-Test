# Claude Test - FastAPI App

A simple REST API built with [FastAPI](https://fastapi.tiangolo.com/) and [yfinance](https://github.com/ranaroussi/yfinance).

## What is FastAPI?

FastAPI is a modern, high-performance Python web framework for building APIs. It is built on top of Starlette (for the web layer) and Pydantic (for data validation). Key features include:

- Automatic interactive API documentation (Swagger UI at `/docs`)
- High performance, on par with Node.js and Go
- Type hints and automatic request/response validation
- Async support out of the box

## What This Project Does

This project exposes the following endpoints:

- **`GET /hello`** — Returns `{"message": "Hello World"}`
- **`GET /stock/{symbol}/now`** — Returns the most recent closing price for the given symbol. Fetches the current time from [timeapi.io](https://timeapi.io) and uses the last 5 trading days to find the latest available price.
- **`GET /stock/{symbol}?date=YYYY-MM-DD`** — Returns the historical closing price for a given stock symbol and date using yfinance. Returns 404 if no data is found (weekends, holidays, or invalid symbols).
- **`GET /crypto/{coin_id}/now`** — Returns the current USD price for a cryptocurrency using the [CoinGecko API](https://www.coingecko.com/en/api). Uses coin IDs like `bitcoin`, `ethereum`, `solana`.
- **`GET /crypto/{coin_id}?date=YYYY-MM-DD`** — Returns the historical USD price for a cryptocurrency on a given date (limited to past 365 days on CoinGecko's free tier).
- **`GET /{anything}`** — Catch-all that echoes back whatever path you send, e.g. `GET /foo` returns `{"message": "foo"}`

## Getting Started

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the server

```bash
uvicorn main:app --reload
```

### Test it

```bash
curl http://localhost:8000/hello
# {"message":"Hello World"}

curl http://localhost:8000/stock/AAPL/now
# {"symbol":"AAPL","date":"2025-02-28","close":241.84}

curl "http://localhost:8000/stock/AAPL?date=2025-01-15"
# {"symbol":"AAPL","date":"2025-01-15","close":236.58}

curl "http://localhost:8000/stock/AAPL?date=2025-01-18"
# 404 — No data found (Saturday)

curl http://localhost:8000/crypto/bitcoin/now
# {"coin":"bitcoin","price":66875.0}

curl "http://localhost:8000/crypto/bitcoin?date=2026-01-15"
# {"coin":"bitcoin","date":"2026-01-15","price":97007.78}

curl http://localhost:8000/goodbye
# {"message":"goodbye"}
```

## Running Tests

Tests use `pytest` with mocked `yfinance` calls so they run fast and offline.

```bash
pytest test_main.py -v
```

## License

This project is licensed under the [GNU Affero General Public License v3.0](LICENSE).
