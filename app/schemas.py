from pydantic import BaseModel
from typing import List, Optional

class ChartDataItem(BaseModel):
    date: str
    open: float
    close: float
    high: float
    low: float

class NewsItem(BaseModel):
    title: str
    summary: str
    link: str
    pubDate: str    # 뉴스 발행 시간
    provider: str   # 뉴스 제공자

class PredictionData(BaseModel):
    horizon: int
    result: str
    confidenceScore: float

class ExplanationData(BaseModel):
    why: str
    shapValues: List[float]
    features: List[str]

class StockInfoResponse(BaseModel):
    ticker: str
    chartData: List[ChartDataItem]
    news: List[NewsItem]
    prediction: PredictionData
    explanation: Optional[ExplanationData]

class StockInfoWrapper(BaseModel):
    success: bool
    message: str
    data: StockInfoResponse
