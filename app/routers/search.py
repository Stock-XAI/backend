# app/routers/search.py
from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from db.session import get_db
from db.models.ticker import Ticker
from sqlalchemy import or_

# S&P 500 시가총액 상위 + 검색량 많은 종목 + 대표 섹터별 종목 조합 50개
POPULAR_TICKERS = [
    "AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META", "NFLX", "BRK-B",
    "JPM", "V", "JNJ", "UNH", "PG", "MA", "HD", "DIS", "ADBE", "PYPL", "BAC",
    "XOM", "INTC", "T", "KO", "PFE", "WMT", "CRM", "CVX", "PEP", "MRK", "ABT",
    "ORCL", "QCOM", "LLY", "CSCO", "MCD", "TMO", "COST", "NKE", "DHR", "ACN",
    "AVGO", "TXN", "AMD", "SBUX", "AMAT", "INTU", "GE", "HON", "ISRG", "BA"
]

router = APIRouter()

# GET /search?keyword=XXX
@router.get("/search")
def search_tickers(
    keyword: Optional[str] = Query(None, description="검색 키워드 (none: all)"),
    db: Session = Depends(get_db)
):
    """
    종목 코드(ticker) 또는 회사 이름(name)으로 자동완성 검색
    - Query param: keyword
    """
    if keyword:
        results = db.query(Ticker).filter(
            or_(
                Ticker.ticker_code.ilike(f"%{keyword}%"),
                Ticker.company_name.ilike(f"%{keyword}%")
            )
        ).limit(10).all()
    else:
        results = db.query(Ticker).filter(Ticker.ticker_code.in_(POPULAR_TICKERS)).all()

    return [
        {
            "ticker": t.ticker_code,
            "name": t.company_name,
            "market": t.market
        }
        for t in results
    ]
