# scripts/test_news.py
"""
- get_recent_news() 가 캐싱/재요청 동작을 잘 수행하는지 테스트
- US(AAPL), KOSPI(005930) 모두 점검
- 기존 캐시가 있는 경우: DB에서 바로 반환
- 캐시 만료되면: yfinance API에서 새로 가져오고 DB 반영됨

실행:
    python scripts/test_news.py
"""

import os
import sys
from datetime import datetime
from pprint import pprint

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)

from db.session import SessionLocal
from app.crud.news import get_recent_news

TEST_TICKERS = ["AAPL", "005930"]  # US / KOSPI

def run_single(ticker_code: str) -> None:
    print(f"\nFetching news for {ticker_code}")
    with SessionLocal() as session:
        articles = get_recent_news(ticker_code, session=session)

    print(f"{len(articles)} articles fetched:")
    for a in articles:
        print(f" - [{a['pubDate']}] {a['title'][:80]}")
        print(f"   {a['link']}")
        print(f"   Provider: {a['provider']}")
        print()

if __name__ == "__main__":
    start = datetime.now()
    for code in TEST_TICKERS:
        run_single(code)
    print(f"\nFinished in {(datetime.now() - start).total_seconds():.2f}s")
