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
        time_response = requests.get("http://worldtimeapi.org/api/timezone/Etc/UTC", timeout=5)
        time_response.raise_for_status()
        utc_now = time_response.json()["datetime"][:10]
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


@app.get("/{path:path}")
def catch_all(path: str):
    return {"message": path}
