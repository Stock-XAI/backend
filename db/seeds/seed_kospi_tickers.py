# db/seeds/seed_kospi_tickers.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import FinanceDataReader as fdr
from sqlalchemy.orm import Session
from db.session import SessionLocal
from db.models.ticker import Ticker

def get_kospi_tickers(limit=50):
    kospi = fdr.StockListing('KOSPI')
    top = kospi.sort_values(by='Marcap', ascending=False).head(limit)
    return top[['Code', 'Name']].reset_index(drop=True)

def seed_kospi_tickers():
    session: Session = SessionLocal()
    tickers = get_kospi_tickers()

    for _, row in tickers.iterrows():
        ticker_code = row['Code']
        name = row['Name']

        existing = session.query(Ticker).filter_by(ticker_code=ticker_code).first()
        if existing:
            existing.company_name = name
        else:
            session.add(Ticker(ticker_code=ticker_code, company_name=name, market='KOSPI'))

    session.commit()
    session.close()
    print("KOSPI tickers inserted into MySQL successfully.")

if __name__ == "__main__":
    seed_kospi_tickers()
