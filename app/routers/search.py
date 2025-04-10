# app/routers/search.py
from fastapi import APIRouter, Query
from typing import Optional
from ..database import db

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
        results = db["tickers"].find(
            { "$or": [ { "ticker": regex }, { "name": regex } ] },
            { "_id": 0 }
        ).limit(10)
    else:
        results = db["tickers"].find({}, { "_id": 0 })
    return list(results)
