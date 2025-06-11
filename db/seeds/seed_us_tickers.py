# db/seeds/seed_us_tickers.py
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import time
import pandas as pd
import yfinance as yf
from sqlalchemy.orm import Session

from db.session import SessionLocal
from db.models.ticker import Ticker

def fix_ticker_format(ticker: str) -> str:
    return ticker.replace(".", "-")

def get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    df = pd.read_html(url)[0]  # S&P 500 테이블
    return df["Symbol"].tolist()

def get_nasdaq_100_tickers():
    url = "https://en.wikipedia.org/wiki/NASDAQ-100"
    df = pd.read_html(url)[4]  # NASDAQ-100 테이블
    return df["Ticker"].tolist()

def fetch_company_name(ticker: str) -> str:
    try:
        info = yf.Ticker(ticker).info
        return info.get("longName") or info.get("shortName")
    except Exception:
        return None

def insert_ticker(db: Session, ticker: str, name: str):
    if not name:
        print(f"{ticker}: null")
        return

    existing = db.query(Ticker).filter(Ticker.ticker_code == ticker).first()
    if existing:
        existing.company_name = name
    else:
        db.add(Ticker(ticker_code=ticker, company_name=name, market="US"))
    db.commit()
    # print(f"{ticker}: {name}")

def seed_us_tickers():
    session = SessionLocal()

    sp500 = get_sp500_tickers()
    nasdaq = get_nasdaq_100_tickers()
    all_tickers = list(set(sp500 + nasdaq))

    for raw in all_tickers:
        ticker = fix_ticker_format(raw)
        name = fetch_company_name(ticker)
        insert_ticker(session, ticker, name)
        time.sleep(0.05)

    session.close()
    print("US tickers inserted into MySQL successfully!")

if __name__ == "__main__":
    seed_us_tickers()