# app/crud/explanation.py
from __future__ import annotations

from typing import Dict, Optional, List
from datetime import date, timedelta

import os
import requests
import json
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from db.session import SessionLocal
from db.models.ticker import Ticker
from db.models.explanation import Explanation
from app.crud.utils import get_session

def generate_explanation(
    ticker_code: str,
    horizon: int,
    session: Session | None = None
) -> Dict[str, object]:
    """
    ticker_code와 horizon_days를 받아 XAI 토큰 중요도 결과를 반환.
    기존 캐시가 있으면 DB에서, 없으면 외부 API에서 받아서 저장.
    반환:
        {
            "predicted_date": str,
            "tokens": List[str],
            "token_scores": List[float]
        }
    """
    with get_session(session) as db:
        pred_date = date.today() + timedelta(days=horizon)

        # Ticker 검증
        ticker: Ticker | None = db.execute(
            select(Ticker).where(Ticker.ticker_code == ticker_code)
        ).scalar_one_or_none()
        if not ticker:
            return {"predicted_date": pred_date, "tokens": [], "token_scores": []}

        # 캐시 조회
        existing: Explanation | None = db.execute(
            select(Explanation)
            .where(
                Explanation.ticker_id == ticker.id,
                Explanation.horizon_days == horizon,
                Explanation.predicted_date == pred_date
            )
        ).scalar_one_or_none()
        if existing:
            return {
                "predicted_date": pred_date,
                "tokens": existing.get_token(),
                "token_scores": existing.get_token_score()
            }

        # API URL 확인 (XAI API)
        api_url = os.getenv("NGROK_API_URL") + "explain"
        if not api_url:
            return {"predicted_date": pred_date, "tokens": [], "token_scores": []}

        # KOSPI 종목이면 .KS 붙여서 보냄
        fetch_code = (
            f"{ticker_code}.KS" if ticker.market.upper() == "KOSPI" else ticker_code
        )

        # 외부 API 호출
        try:
            resp = requests.get(
                api_url,
                params={"ticker": fetch_code, "horizon_days": horizon},
                headers={"ngrok-skip-browser-warning": "true"},
                timeout=60
            )
            resp.raise_for_status()
            payload = resp.json()
        except Exception as e:
            print("XAI API error:", e)
            return {"predicted_date": pred_date, "tokens": [], "token_scores": []}

        tokens = payload.get("token_list", [])
        token_scores = payload.get("token_score_list", [])

        # Attempt to insert into DB
        try:
            explain = Explanation(
                ticker_id=ticker.id,
                predicted_date=pred_date,
                horizon_days=horizon,
            )
            explain.set_token(tokens)
            explain.set_token_score(token_scores)
            db.add(explain)
            db.commit()
        except IntegrityError:
            # Race condition: another process inserted same record
            db.rollback()
            
            existing = db.execute(
                select(Explanation).where(
                    Explanation.ticker_id == ticker.id,
                    Explanation.horizon_days == horizon,
                    Explanation.predicted_date == pred_date
                )
            ).scalar_one_or_none()

            if existing:
                return {
                    "predicted_date": pred_date,
                    "tokens": existing.get_token(),
                    "token_scores": existing.get_token_score()
                }

            # Fallback if still not found
            return {"predicted_date": pred_date, "tokens": [], "token_scores": []}

        return {
            "predicted_date": pred_date,
            "tokens": tokens,
            "token_scores": token_scores
        }
