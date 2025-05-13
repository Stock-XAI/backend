# app/crud.py
from typing import List, Dict
import yfinance as yf
import FinanceDataReader as fdr
from datetime import datetime, timedelta

# 주가 데이터 조회
def get_chart_data(ticker: str, market: str = "US") -> List[Dict]:
    if market == "KOSPI":
        return get_kospi_chart_data(ticker)
    else:
        return get_us_chart_data(ticker)
    
# 미국 주식이면 yfinance로 가져오기
def get_us_chart_data(ticker: str) -> List[Dict]:
    ticker_data = yf.Ticker(ticker)
    data = ticker_data.history(period="1mo")
    if not data.empty:
        # 소수점 2자리로 반올림
        data = data.round(2)
        chart_data = [
            {
                "date": str(date.date()),
                "open": row["Open"],
                "close": row["Close"],
                "high": row["High"],
                "low": row["Low"],
                # "volume": row["Volume"],
            }
            for date, row in data.iterrows()
        ]
        return chart_data
    else:
        return []
    
# 한국 주식이면 FDR로 가져오기
def get_kospi_chart_data(ticker: str) -> List[Dict]:
    try:
        today = datetime.today()
        one_month_ago = today - timedelta(days=30)
        
        df = fdr.DataReader(ticker, start=one_month_ago.strftime("%Y-%m-%d"))
        df = df.round(2)
        
        return [
            {
                "date": str(date.date()),
                "open": row["Open"],
                "close": row["Close"],
                "high": row["High"],
                "low": row["Low"],
            }
            for date, row in df.iterrows()
        ]
    except Exception:
        return []

# 뉴스 요약 데이터
def get_recent_news(ticker: str, market: str = "US") -> List[Dict]:
    if market == "US":
        return get_us_news(ticker)
    elif market == "KOSPI":
        return get_kospi_news(ticker)
    else:
        return []
    
# US 뉴스 요약 데이터
def get_us_news(ticker: str) -> List[Dict]:
    try:
        ticker_data = yf.Ticker(ticker)
        news = ticker_data.news
        parsed_news = []

        for article in news:
            content = article.get('content', {})
            title = content.get('title')
            url_info = content.get('canonicalUrl', {})
            link = url_info.get('url')
            pubDate = content.get('pubDate', "")
            provider_info = content.get('provider', {})
            provider = provider_info.get('displayName', "")

            if title and link:
                parsed_news.append({
                    "title": title,
                    "summary": content.get('summary', ""),
                    "link": link,
                    "pubDate": pubDate,
                    "provider": provider
                })

        return parsed_news[:10]

    except Exception as e:
        print(f"Error fetching US news for {ticker}: {e}")
        return []

"""
# KOSPI 종목도 .KS 붙여서 시도 
# TODO: 한국어 뉴스가 제공되지 않기에 RAG나 다른 방법 고려려
"""
def get_kospi_news(ticker: str) -> List[Dict]:
    try:
        ticker_with_ks = ticker + ".KS"
        ticker_data = yf.Ticker(ticker_with_ks)
        news = ticker_data.news
        parsed_news = []

        for article in news:
            content = article.get('content', {})
            title = content.get('title')
            url_info = content.get('canonicalUrl', {})
            link = url_info.get('url')
            pubDate = content.get('pubDate', "")
            provider_info = content.get('provider', {})
            provider = provider_info.get('displayName', "")

            if title and link:
                parsed_news.append({
                    "title": title,
                    "summary": content.get('summary', ""),
                    "link": link,
                    "pubDate": pubDate,
                    "provider": provider
                })

        if parsed_news:
            return parsed_news[:10]
        else:
            return [{
                "title": f"{ticker} 관련 뉴스 없음",
                "summary": "",
                "link": "",
                "pubDate": "",
                "provider": ""
            }]

    except Exception as e:
        print(f"Error fetching KOSPI news for {ticker}: {e}")
        return [{
            "title": f"{ticker} 관련 뉴스 없음",
            "summary": "",
            "link": "",
            "pubDate": "",
            "provider": ""
        }]

# 예측 결과 생성
import os, requests
def run_prediction(ticker: str, horizon: int) -> Dict:
    api_url = os.getenv("NGROK_API_URL")
    if not api_url:
        return {"error": "NGROK_API_URL not set"}
    
    res = requests.get(
        api_url,
        params={"ticker": ticker, "horizon_days": horizon},
        headers={"ngrok-skip-browser-warning": "true"}
    )
    
    if res.status_code != 200:
        return {"error": f"API error: {res.status_code}"}

    data = res.json()
    return {
        "horizon": horizon,
        "result": data.get("prediction_result", "N/A")
    }

# XAI 해석 결과 (SHAP, LIME 등 연동 예정)
def generate_explanation(ticker: str, horizon: int) -> Dict:
    return {
        "why": "주가 상승 요인은 거래량 증가 및 단기 이동평균 우위",
        "shapValues": [0.12, -0.07],
        "features": ["MA_5", "Volume"]
    }
