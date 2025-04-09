# app/routers/stock.py
from fastapi import APIRouter, Query, HTTPException
from ..crud import *
from ..database import db
from ..schemas import StockInfoResponse, StockInfoWrapper

router = APIRouter()

# GET /stock-info
@router.get("/stock-info", response_model=StockInfoWrapper)
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

    # 유효한 티커인지 MongoDB에서 확인
    if not db["tickers"].find_one({"ticker": ticker}):
        raise HTTPException(status_code=404, detail="해당 티커 정보를 찾을 수 없습니다.")
    
    # 차트 데이터 (Mock)
    chart_data = get_chart_data(ticker)

    # 뉴스 데이터 (Mock)
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