# db/init_db.py
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.session import engine, Base
from db.models import ticker, chart_data, prediction, news

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("All tables created.")
