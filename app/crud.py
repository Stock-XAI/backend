# app/crud.py

from typing import List, Dict

# 주가 데이터 조회 (mock)
def get_chart_data(ticker: str) -> List[Dict]:
    return [
        {"date": "2025-04-01", "open": 170.2, "close": 172.5},
        {"date": "2025-04-02", "open": 172.5, "close": 173.1},
    ]

# 뉴스 요약 데이터 (mock or 실제 RAG 대체 가능)
def get_recent_news(ticker: str) -> List[Dict]:
    return [
        {
            "title": f"{ticker} releases new product",
            "summary": "애플이 새로운 제품을 출시했습니다.",
            "sentiment": "positive"
        },
        {
            "title": f"{ticker} faces supply chain issue",
            "summary": "공급망 이슈로 인한 주가 변동 가능성 언급.",
            "sentiment": "negative"
        }
    ]

# 예측 결과 생성 (향후 모델 연동)
def run_prediction(ticker: str, horizon: int) -> Dict:
    return {
        "horizon": horizon,
        "result": "Rise",  # or "Fall"
        "confidenceScore": 0.86
    }

# XAI 해석 결과 (SHAP, LIME 등 연동 예정)
def generate_explanation(ticker: str, horizon: int) -> Dict:
    return {
        "why": "주가 상승 요인은 거래량 증가 및 단기 이동평균 우위",
        "shapValues": [0.12, -0.07],
        "features": ["MA_5", "Volume"]
    }
