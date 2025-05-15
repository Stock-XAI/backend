# scripts/test_prediction.py
"""
- run_prediction() 이 실제로 API 호출 → DB 저장 → 캐싱 동작을 올바르게 하는지 테스트
- 첫 호출: 외부 API 호출
- 두 번째 호출: DB 캐시 반환
- US(AAPL) 와 KOSPI(005930) 모두 점검

실행:
    NGROK_API_URL=http://<your-ngrok-url>/predict \
    python scripts/test_prediction.py
"""

import os
import sys
import time
from pprint import pprint
from datetime import datetime

# 프로젝트 루트 추가
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)

from db.session import SessionLocal
from app.crud.prediction import run_prediction

# 테스트 대상 티커 + horizon_days 리스트
TEST_CASES = [
    ("AAPL", 1),     # US
    ("005930", 1),   # KOSPI
    ("AAPL", 7),     # US
    ("005930", 7),   # KOSPI
    ("AAPL", 30),     # US
    ("005930", 30),   # KOSPI
]

def run_single(ticker: str, horizon: int) -> None:
    print(f"\n=== Testing {ticker} (+{horizon}d) ===")

    # 첫 호출: API → DB 저장
    start = time.time()
    with SessionLocal() as session:
        result1 = run_prediction(ticker, horizon, session=session)
    t1 = time.time() - start

    # 두 번째 호출: DB 캐시
    start = time.time()
    with SessionLocal() as session:
        result2 = run_prediction(ticker, horizon, session=session)
    t2 = time.time() - start

    print(f"[1st call]  elapsed: {t1:.3f}s")
    pprint(result1)
    print(f"[2nd call]  elapsed: {t2:.3f}s")
    pprint(result2)


if __name__ == "__main__":
    overall_start = datetime.now()
    for code, h in TEST_CASES:
        run_single(code, h)
    total = (datetime.now() - overall_start).total_seconds()
    print(f"\nAll tests finished in {total:.2f}s")
