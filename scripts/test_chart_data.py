# scripts/test_chart_data.py
"""
- get_chart_data() 가 캐싱·API fetch를
  제대로 수행하는지 눈으로 확인
- US(AAPL) / KOSPI(005930.KS) 모두 점검
- interval = 1, 7, 30 순회

실행:
    python scripts/test_chart_data.py
"""

import os
import sys
from datetime import datetime
from pprint import pprint

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)

from db.session import SessionLocal
from app.crud.chart import get_chart_data

TEST_CASES = [
    ("AAPL",    1),
    ("005930",  1),
    ("AAPL",    7),
    ("005930",  7),
    ("AAPL",   30),
    ("005930", 30),
]

def run_single(ticker_code: str, interval: int) -> None:
    print(f"\nFetching {ticker_code}  interval={interval}")
    with SessionLocal() as session:
        rows = get_chart_data(ticker_code, interval=interval, session=session)

    print(f"{len(rows)} rows fetched (show last 3):")
    for r in rows[-3:]:
        pprint(r)

if __name__ == "__main__":
    start = datetime.now()
    for tc in TEST_CASES:
        run_single(*tc)
    print(f"\nFinished in {(datetime.now() - start).total_seconds():.2f}s")
