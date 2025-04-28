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

# 3. 한국 KOSPI 시가총액 상위 종목 가져오기
def get_kospi_tickers(limit=50):
    kospi = fdr.StockListing('KOSPI')
    top = kospi.sort_values(by='Marcap', ascending=False).head(limit)
    return top[['Symbol', 'Name']].reset_index(drop=True)

# 4. MongoDB에 티커 삽입
def insert_ticker(ticker: str, name: str):
    if not ticker or not name:
        print(f"❌ Invalid data: {ticker} - {name}")
        return
    collection.update_one(
        {"ticker": ticker},
        {"$set": {"ticker": ticker, "name": name}},
        upsert=True
    )
    print(f"✅ Inserted: {ticker} - {name}")

# 5. 메인 실행
if __name__ == "__main__":
    kospi_tickers = get_kospi_tickers(limit=50)  # 필요하면 limit=200 가능

    for idx, row in kospi_tickers.iterrows():
        ticker = row["Symbol"]
        name = row["Name"]
        insert_ticker(ticker, name)
        time.sleep(0.2)  # 서버 과부하 방지

    print("🎉 KOSPI tickers inserted into MongoDB successfully!")
