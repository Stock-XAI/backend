# app/routers/stock.py
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from .. import schemas

router = APIRouter()

# GET /stock-info
@router.get("/stock-info")
def get_stock_info(
    ticker: str = Query(..., description="종목 코드 (예: AAPL)"),
    horizon: int = Query(7, description="예측 기간 (1, 7, 30일 등)"),
    includeNews: bool = Query(True, description="뉴스 포함 여부"),
    includeXAI: bool = Query(True, description="XAI 해석 포함 여부")
):
    """
    주가 예측 결과 및 해석 제공 API
    - ticker: 주식 코드
    - horizon: 예측 기간 (일)
    - includeNews: 뉴스 요약 포함 여부
    - includeXAI: 예측 결과 해석 포함 여부
    """

    # 유효한 티커인지 확인 (Mock)
    valid_tickers = ["AAPL", "MSFT", "GOOG"]
    if ticker not in valid_tickers:
        raise HTTPException(status_code=404, detail="해당 티커 정보를 찾을 수 없습니다.")

    # 모의 차트 데이터
    chart_data = [
        {"date": "2025-04-01", "open": 170.2, "close": 172.5},
        {"date": "2025-04-02", "open": 172.5, "close": 173.1},
    ]

    # 모의 뉴스 데이터
    news_data = []
    if includeNews:
        news_data = [
            {"title": f"{ticker} releases new product", "summary": "주요 기사 요약...", "sentiment": "positive"},
            {"title": f"{ticker} faces supply chain issue", "summary": "또 다른 기사 요약...", "sentiment": "negative"}
        ]

    # 예측 결과 (Mock)
    prediction = {
        "horizon": horizon,
        "result": "Rise",
        "confidenceScore": 0.86
    }

    # 예측 해석 (Mock)
    explanation = {}
    if includeXAI:
        explanation = {
            "why": "주가 상승 요인은 거래량 증가 및 단기 이동평균 우위",
            "shapValues": [0.12, -0.07],
            "features": ["MA_5", "Volume"]
        }

    return {
        "success": True,
        "message": "Stock info fetched",
        "data": {
            "ticker": ticker,
            "chartData": chart_data,
            "news": news_data,
            "prediction": prediction,
            "explanation": explanation
        }
    }
