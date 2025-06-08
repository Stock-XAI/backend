# app/routers/stock.py
from fastapi import APIRouter, Query, HTTPException
from app.crud import *
from app.schemas import ChartAndNewsResponse, PredictionResponse, ExplanationResponse
router = APIRouter()

# GET /stock-info/basic
@router.get("/stock-info/basic", response_model=ChartAndNewsResponse)
def get_stock_basic(
    ticker: str = Query(..., description="종목 코드 (예: AAPL, 005930)"),
    horizon: int = Query(7, description="예측 기간 (1, 7, 30일 등)")
):
    if horizon not in (1, 7, 30):
        raise HTTPException(status_code=400, detail="horizon must be 1, 7, or 30")
    
    chart_data = get_chart_data(ticker, interval=horizon)
    news_data = get_recent_news(ticker)

    return ChartAndNewsResponse(
        ticker=ticker,
        chartData=chart_data,
        news=news_data
    )

# GET /stock-info/pred
@router.get("/stock-info/pred", response_model=PredictionResponse)
def get_prediction(
    ticker: str = Query(..., description="종목 코드 (예: AAPL, 005930)"),
    horizon: int = Query(7, description="예측 기간 (1, 7, 30일 등)")
):
    if horizon not in (1, 7, 30):
        raise HTTPException(status_code=400, detail="horizon must be 1, 7, or 30")

    prediction = run_prediction(ticker, horizon)

    return PredictionResponse(
        ticker=ticker,
        prediction=prediction
    )

# GET /stock-info/exp
@router.get("/stock-info/exp", response_model=ExplanationResponse)
def get_explanation(
    ticker: str = Query(..., description="종목 코드 (예: AAPL, 005930)"),
    horizon: int = Query(7, description="예측 기간 (1, 7, 30일 등)")
):
    if horizon not in (1, 7, 30):
        raise HTTPException(status_code=400, detail="horizon must be 1, 7, or 30")

    explanation = generate_explanation(ticker, horizon)

    return ExplanationResponse(
        ticker=ticker,
        explanation=explanation
    )