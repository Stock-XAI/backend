# scripts/seed_kospi_tickers.py
import FinanceDataReader as fdr
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
collection = client["db"]["tickers_kospi"]

def get_kospi_tickers(limit=50):
    kospi = fdr.StockListing('KOSPI')
    top = kospi.sort_values(by='Marcap', ascending=False).head(limit)
    return top[['Code', 'Name']].reset_index(drop=True)

def insert_ticker(ticker: str, name: str):
    if not ticker or not name:
        print(f"{ticker} - {name}")
        return
    collection.update_one(
        {"ticker": ticker},
        {"$set": {"ticker": ticker, "name": name}},
        upsert=True
    )
    print(f"{ticker} - {name}")

if __name__ == "__main__":
    kospi_tickers = get_kospi_tickers(limit=50)

    for idx, row in kospi_tickers.iterrows():
        ticker = row["Code"]
        name = row["Name"]
        insert_ticker(ticker, name)
        time.sleep(0.2)

    print("KOSPI tickers inserted into MongoDB successfully!")
