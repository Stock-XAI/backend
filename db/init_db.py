# db/init_db.py
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.session import engine, Base
from db.models import explanation, ticker, chart_data, prediction, news

from db.seeds.seed_kospi_tickers import seed_kospi_tickers
from db.seeds.seed_us_tickers import seed_us_tickers

if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    print("Dropped all tables.")
    
    Base.metadata.create_all(bind=engine)
    print("All tables created.")

    seed_kospi_tickers()
    seed_us_tickers()
    print("All seed data inserted.")