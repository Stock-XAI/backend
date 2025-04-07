# app/routers/search.py
from fastapi import APIRouter, Query
from ..database import db

router = APIRouter()

# GET /search?t=XXX
@router.get("/search")
def search_tickers(t: str = Query(..., description="검색 키워드")):
    """
    종목 코드(ticker) 또는 회사 이름(name)으로 자동완성 검색
    - Query param: t
    """
    regex = {"$regex": t, "$options": "i"}
    results = db["tickers"].find(
        { "$or": [ { "ticker": regex }, { "name": regex } ] },
        { "_id": 0 }
    ).limit(10)
    return list(results)
