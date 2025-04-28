# app/routers/search.py
from fastapi import APIRouter, Query
from typing import Optional
from ..database import db

# S&P 500 시가총액 상위 + 검색량 많은 종목 + 대표 섹터별 종목 조합 50개
POPULAR_TICKERS = [
    "AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META", "NFLX", "BRK-B",
    "JPM", "V", "JNJ", "UNH", "PG", "MA", "HD", "DIS", "ADBE", "PYPL", "BAC",
    "XOM", "INTC", "T", "KO", "PFE", "WMT", "CRM", "CVX", "PEP", "MRK", "ABT",
    "ORCL", "QCOM", "LLY", "CSCO", "MCD", "TMO", "COST", "NKE", "DHR", "ACN",
    "AVGO", "TXN", "AMD", "SBUX", "AMAT", "INTU", "GE", "HON", "ISRG", "BA"
]

router = APIRouter()

# GET /search?t=XXX
@router.get("/search")
def search_tickers(keyword: Optional[str] = Query(None, description="검색 키워드 (none: all)")):
    """
    종목 코드(ticker) 또는 회사 이름(name)으로 자동완성 검색
    - Query param: keyword
    """
    if keyword:
        regex = {"$regex": keyword, "$options": "i"}
        results = db["tickers_us"].find(
            { "$or": [ { "ticker": regex }, { "name": regex } ] },
            { "_id": 0 }
        ).limit(10)
    else:
        results = db["tickers_us"].find(
            { "ticker": { "$in": POPULAR_TICKERS } },
            { "_id": 0 }
        )
    return list(results)
