from datetime import datetime, timedelta

import yfinance as yf
from fastapi import FastAPI, HTTPException, Query

app = FastAPI()


@app.get("/hello")
def hello_world():
    return {"message": "Hello World"}


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
