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
- **`GET /stock/{symbol}?date=YYYY-MM-DD`** — Returns the historical closing price for a given stock symbol and date using yfinance. Returns 404 if no data is found (weekends, holidays, or invalid symbols).
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

curl "http://localhost:8000/stock/AAPL?date=2025-01-15"
# {"symbol":"AAPL","date":"2025-01-15","close":236.58}

curl "http://localhost:8000/stock/AAPL?date=2025-01-18"
# 404 — No data found (Saturday)

curl http://localhost:8000/goodbye
# {"message":"goodbye"}
```

## License

This project is licensed under the [GNU Affero General Public License v3.0](LICENSE).
