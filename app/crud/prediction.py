# app/crud/prediction.py
from __future__ import annotations

from typing import Dict, Optional, List
from datetime import date, timedelta

import os
import requests
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from db.session import SessionLocal
from db.models.ticker import Ticker
from db.models.prediction import Prediction

from app.crud.utils import get_session

def run_prediction(
    ticker_code: str,
    horizon: int,
    session: Session | None = None
) -> Dict[str, object]:
    """
    ticker_code와 horizon_days를 받아 예측 결과를 반환합니다.
    기존 캐시가 있으면 DB에서 가져오고, 없으면 외부 API 호출 후 DB에 저장 후 반환합니다.

    반환 형식:
        {
            "predicted_date": str,
            "result": float
        }
    """
    with get_session(session) as db:
        pred_date = date.today() + timedelta(days=horizon)
        
        # Ticker 검증
        ticker: Ticker | None = db.execute(
            select(Ticker).where(Ticker.ticker_code == ticker_code)
        ).scalar_one_or_none()
        if not ticker:
            return {"predicted_date": pred_date.isoformat(), "result": 0.0}

        # 캐시 조회
        existing: Prediction | None = db.execute(
            select(Prediction)
            .where(
                Prediction.ticker_id == ticker.id,
                Prediction.horizon_days == horizon,
                Prediction.predicted_date == pred_date
            )
        ).scalar_one_or_none()
        if existing:
            return {"predicted_date": pred_date.isoformat(), "result": existing.prediction_result}

        # API URL 확인
        api_url = os.getenv("NGROK_API_URL") + "predict"
        if not api_url:
            return {"predicted_date": pred_date.isoformat(), "result": 0.0}

        # KOSPI 종목이면 .KS 붙여서 보냄
        fetch_code = (
            f"{ticker_code}.KS" if ticker.market.upper() == "KOSPI" else ticker_code
        )
        
        # 외부 API 호출
        try:
            print(api_url)
            print(fetch_code)
            resp = requests.get(
                api_url,
                params={"ticker": fetch_code, "horizon_days": horizon},
                headers={"ngrok-skip-browser-warning": "true"},
                timeout=60
            )
            resp.raise_for_status()
            payload = resp.json()
        except Exception as e:
            print("XAI API 안 띄웠거나 주소 잘못됨:", e)
            return {"predicted_date": pred_date.isoformat(), "result": 0.0}

        result = payload.get("prediction_result", 0.0)

        # Insert into DB with exception safety
        try:
            pred = Prediction(
                ticker_id=ticker.id,
                predicted_date=pred_date,
                horizon_days=horizon,
                prediction_result=result
            )
            db.add(pred)
            db.commit()
        except IntegrityError:
            db.rollback()
            existing = db.execute(
                select(Prediction)
                .where(
                    Prediction.ticker_id == ticker.id,
                    Prediction.horizon_days == horizon,
                    Prediction.predicted_date == pred_date
                )
            ).scalar_one_or_none()

            if existing:
                return {"predicted_date": pred_date.isoformat(), "result": existing.prediction_result}
            return {"predicted_date": pred_date.isoformat(), "result": 0.0}

        return {
            "predicted_date": pred_date.isoformat(),
            "result": result
        }