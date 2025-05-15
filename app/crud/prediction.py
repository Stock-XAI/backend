# app/crud/prediction.py
from __future__ import annotations

from typing import Dict, Optional, List
from contextlib import contextmanager
from datetime import date, timedelta

import os
import requests
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.session import SessionLocal
from db.models.ticker import Ticker
from db.models.prediction import Prediction


@contextmanager
def _get_session(ext_session: Optional[Session] = None):
    if ext_session:
        yield ext_session
    else:
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()


def run_prediction(
    ticker_code: str,
    horizon: int,
    *,
    session: Session | None = None
) -> Dict[str, object]:
    """
    ticker_code와 horizon_days를 받아 예측 결과를 반환합니다.
    기존 캐시가 있으면 DB에서 가져오고, 없으면 외부 API 호출 후 DB에 저장 후 반환합니다.

    반환 형식:
        {
            "horizon": int,
            "result": str
        }
    """
    with _get_session(session) as db:
        # Ticker 검증
        ticker: Ticker | None = db.execute(
            select(Ticker).where(Ticker.ticker_code == ticker_code)
        ).scalar_one_or_none()
        if not ticker:
            return {"horizon": horizon, "result": ""}

        # 캐시 조회
        pred_date = date.today() + timedelta(days=horizon)
        existing: Prediction | None = db.execute(
            select(Prediction)
            .where(
                Prediction.ticker_id == ticker.id,
                Prediction.horizon_days == horizon,
                Prediction.predicted_date == pred_date
            )
        ).scalar_one_or_none()
        if existing:
            return {"horizon": horizon, "result": existing.prediction_result}

        # API URL 확인
        api_url = os.getenv("NGROK_API_URL")
        if not api_url:
            return {"horizon": horizon, "result": ""}

        # 외부 API 호출
        try:
            resp = requests.get(
                api_url,
                params={"ticker": ticker_code, "horizon_days": horizon},
                headers={"ngrok-skip-browser-warning": "true"},
                timeout=10
            )
            resp.raise_for_status()
            payload = resp.json()
        except Exception:
            print("API 없는데요?")
            return {"horizon": horizon, "result": ""}

        result = payload.get("prediction_result", "")

        # DB에 저장
        pred = Prediction(
            ticker_id=ticker.id,
            predicted_date=pred_date,
            horizon_days=horizon,
            prediction_result=result
        )
        db.add(pred)
        db.commit()

        return {"horizon": horizon, "result": result}


def get_predicted(
    ticker_code: str,
    horizon: Optional[int] = None,
    limit: int = 10,
    *,
    session: Session | None = None
) -> List[Dict[str, object]]:
    """
    DB에 저장된 예측 결과를 조회합니다.
    - horizon을 지정하면 해당 기간 필터링
    - 없으면 최근 limit개 반환

    반환 형식: List of {"horizon": int, "result": str}
    """
    with _get_session(session) as db:
        ticker: Ticker | None = db.execute(
            select(Ticker).where(Ticker.ticker_code == ticker_code)
        ).scalar_one_or_none()
        if not ticker:
            return []

        # 쿼리 빌드
        query = select(Prediction).where(Prediction.ticker_id == ticker.id)
        if horizon is not None:
            query = query.where(Prediction.horizon_days == horizon)
        query = query.order_by(Prediction.predicted_date.desc()).limit(limit)

        rows = db.execute(query).scalars().all()
        return [
            {"horizon": row.horizon_days, "result": row.prediction_result}
            for row in rows
        ]
