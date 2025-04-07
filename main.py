# main.py
from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI(
    title="Stock Info API",
    description="A simple FastAPI service that returns stock info, news, predictions, etc.",
    version="0.1.0"
)

# -----------------------------
# 데이터 모델 (Pydantic) 예시
# -----------------------------
class ChartDataItem(BaseModel):
    date: str
    open: float
    close: float

class NewsItem(BaseModel):
    title: str
    summary: str
    sentiment: str

class PredictionData(BaseModel):
    horizon: int
    result: str
    confidenceScore: float

class ExplanationData(BaseModel):
    why: str
    shapValues: list
    features: list

class StockInfoResponse(BaseModel):
    ticker: str
    chartData: list[ChartDataItem]
    news: list[NewsItem]
    prediction: PredictionData
    explanation: ExplanationData

# -----------------------------
# 임시 Mock 데이터/함수
# -----------------------------
def get_mock_chart_data(ticker: str):
    # 실제로는 DB나 yfinance 등에서 과거 주가 데이터를 가져오면 됨
    return [
        {"date": "2025-04-01", "open": 170.2, "close": 172.5},
        {"date": "2025-04-02", "open": 172.5, "close": 173.1},
    ]

def get_mock_news(ticker: str):
    # 실제 뉴스가 아니라 간단한 예시
    return [
        {"title": f"{ticker} releases new product", "summary": "주요 기사 요약...", "sentiment": "positive"},
        {"title": f"{ticker} faces supply chain issue", "summary": "또 다른 기사 요약...", "sentiment": "negative"}
    ]

def run_mock_prediction(ticker: str, horizon: int, include_xai: bool):
    # 실제 모델 대신, 단순히 "Rise" or "Fall" 임의로 리턴
    return {
        "horizon": horizon,
        "result": "Rise",
    }

def run_mock_explanation(ticker: str, horizon: int):
    # SHAP, LIME 등 xai 대신 임시 결과
    return {
        "why": "Short reason from the model about why it predicted Rise",
        "shapValues": [0.12, -0.07],
        "features": ["MA_5", "volume"]
    }

# -----------------------------
# Endpoint
# -----------------------------
@app.get("/stock-info")
def get_stock_info(
    ticker: str = Query(..., description="종목 코드 (예: AAPL)"),
    horizon: int = Query(7, description="예측 기간 (예: 1, 7, 30)"),
    includeNews: bool = Query(True, description="뉴스 데이터 포함 여부"),
    includeXAI: bool = Query(True, description="해석 정보 포함 여부")
):
    """
    GET /stock-info?ticker=AAPL&horizon=7&includeNews=true&includeXAI=true
    위 쿼리 파라미터를 받아, 주가 차트/뉴스/예측 결과/해석 정보를 모두 반환
    """

    # 1) ticker 유효성 확인 (mock로는 AAPL, MSFT만 허용 예시)
    valid_tickers = ["AAPL", "MSFT"]
    if ticker not in valid_tickers:
        return {
            "success": False,
            "message": f"해당 티커 정보를 찾을 수 없습니다: {ticker}",
            "data": None
        }

    # 2) 차트 데이터 조회 (mock)
    chart_data = get_mock_chart_data(ticker)

    # 3) 뉴스 조회 (옵션)
    news_data = get_mock_news(ticker) if includeNews else []

    # 4) 예측 결과 산출 (mock)
    pred_result = run_mock_prediction(ticker, horizon, includeXAI)

    # 5) 해석(XAI) 정보 (옵션)
    expl_data = run_mock_explanation(ticker, horizon) if includeXAI else {}

    # 6) 최종 데이터 구성
    response_data = {
        "ticker": ticker,
        "chartData": chart_data,
        "news": news_data,
        "prediction": pred_result,
        "explanation": expl_data
    }

    return {
        "success": True,
        "message": "Stock info fetched",
        "data": response_data
    }
