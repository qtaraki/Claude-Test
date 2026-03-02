from datetime import datetime, timedelta

import requests
import yfinance as yf
from fastapi import FastAPI, HTTPException, Query

app = FastAPI()


@app.get("/hello")
def hello_world():
    return {"message": "Hello World"}


@app.get("/stock/{symbol}/now")
def get_current_stock_price(symbol: str):
    try:
        time_response = requests.get("https://timeapi.io/api/time/current/zone?timeZone=UTC", timeout=5)
        time_response.raise_for_status()
        utc_now = time_response.json()["dateTime"][:10]
    except Exception:
        raise HTTPException(status_code=503, detail="Unable to fetch current time from time server")

    ticker = yf.Ticker(symbol)
    history = ticker.history(period="5d")

    if history.empty:
        raise HTTPException(status_code=404, detail=f"No data found for {symbol}")

    last_row = history.iloc[-1]
    trade_date = str(history.index[-1].date())
    close_price = round(float(last_row["Close"]), 2)
    return {"symbol": symbol.upper(), "date": trade_date, "close": close_price}


@app.get("/stock/{symbol}")
def get_stock_price(symbol: str, date: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$")):
    try:
        request_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    next_date = request_date + timedelta(days=1)
    ticker = yf.Ticker(symbol)
    history = ticker.history(start=request_date.strftime("%Y-%m-%d"), end=next_date.strftime("%Y-%m-%d"))

    if history.empty:
        raise HTTPException(status_code=404, detail=f"No data found for {symbol} on {date}")

    close_price = round(float(history["Close"].iloc[0]), 2)
    return {"symbol": symbol.upper(), "date": date, "close": close_price}


COINGECKO_BASE = "https://api.coingecko.com/api/v3"


@app.get("/crypto/{coin_id}/now")
def get_current_crypto_price(coin_id: str):
    response = requests.get(f"{COINGECKO_BASE}/simple/price", params={"ids": coin_id, "vs_currencies": "usd"}, timeout=5)
    data = response.json()

    if coin_id not in data:
        raise HTTPException(status_code=404, detail=f"No data found for {coin_id}")

    price = round(float(data[coin_id]["usd"]), 2)
    return {"coin": coin_id, "price": price}


@app.get("/crypto/{coin_id}")
def get_historical_crypto_price(coin_id: str, date: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$")):
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    cg_date = parsed_date.strftime("%d-%m-%Y")
    response = requests.get(f"{COINGECKO_BASE}/coins/{coin_id}/history", params={"date": cg_date}, timeout=10)

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"No data found for {coin_id}")

    data = response.json()
    if "market_data" not in data:
        raise HTTPException(status_code=404, detail=f"No data found for {coin_id} on {date}")

    price = round(float(data["market_data"]["current_price"]["usd"]), 2)
    return {"coin": coin_id, "date": date, "price": price}


@app.get("/{path:path}")
def catch_all(path: str):
    return {"message": path}
