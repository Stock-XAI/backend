# scripts/seed_sp500_tickers.py
import yfinance as yf
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import time

load_dotenv()
db_password = os.getenv("DB_PASSWORD")
if not db_password:
    raise ValueError("DB_PASSWORD is not set in .env")

MONGO_URI = f"mongodb+srv://skkucapstone:{db_password}@stock.iz5b97b.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
collection = client["db"]["tickers"]

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
    
def insert_ticker(ticker: str, name: str):
    if not name:
        print(f"{ticker}: null")
        return
    collection.update_one(
        {"ticker": ticker},
        {"$set": {"ticker": ticker, "name": name}},
        upsert=True
    )
    print(f"{ticker}: {name}")
    
if __name__ == "__main__":
    sp500 = get_sp500_tickers()
    nasdaq = get_nasdaq_100_tickers()
    all_tickers = list(set(sp500 + nasdaq))
    
    for raw in all_tickers:
        ticker = fix_ticker_format(raw)
        name = fetch_company_name(ticker)
        insert_ticker(ticker, name)
        time.sleep(0.2)

    print("티커 + 회사 이름 MongoDB 저장 완료")