# app/routers/stock.py
from fastapi import APIRouter, Query, HTTPException
from app.crud import *
from app.schemas import StockInfoResponse, StockInfoWrapper

router = APIRouter()

# GET /stock-info
@router.get("/stock-info", response_model=StockInfoWrapper)
def get_stock_info(
    ticker: str = Query(..., description="종목 코드 (예: AAPL, 005930)"),
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

    # 차트 데이터
    chart_data = get_chart_data(ticker, interval=horizon)

    # 뉴스 데이터
    news_data = get_recent_news(ticker) if includeNews else []

    # 예측 결과 (Mock)
    prediction = run_prediction(ticker, horizon)

    # 예측 해석 (Mock)
    explanation = generate_explanation(ticker, horizon) if includeXAI else {}

    return StockInfoWrapper(
        success=True,
        message="Stock info fetched",
        data=StockInfoResponse(
            ticker=ticker,
            chartData=chart_data,
            news=news_data,
            prediction=prediction,
            explanation=explanation
        )
    )