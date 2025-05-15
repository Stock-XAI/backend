# app/crud/chart.py
"""Chart-data CRUD + caching logic.

Key design points:
Incremental fetch - DB에 없는 최신 구간만 외부 API로 가져와 cache
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List, Dict

import yfinance as yf
import FinanceDataReader as fdr
from sqlalchemy import select, and_, func
from sqlalchemy.orm import Session

from db.session import SessionLocal
from db.models.chart_data import ChartData
from db.models.ticker import Ticker

from contextlib import contextmanager

@contextmanager
def _get_session(ext_session: Session | None):
    if ext_session is not None:
        yield ext_session
    else:
        s = SessionLocal()
        try:
            yield s
        finally:
            s.close()
            
# ──────────────────────────────────────────────────────────────────────────────
# public api
# ──────────────────────────────────────────────────────────────────────────────

def get_chart_data(ticker_code: str,
                   *, 
                   interval: int = 1,
                   session: Session | None = None) -> List[Dict]:
    """Return cached+fresh chart rows for ticker_code.

    If DB is missing rows after the latest cached date, we fetch only that gap
    from the appropriate data source (yfinance for US / FDR for KOSPI) and then
    persist them.  Supported interval days: 1, 7, 30.
    """
    if interval not in (1, 7, 30):
        raise ValueError("interval must be 1, 7 or 30")

    with _get_session(session) as db:
        ticker: Ticker | None = (
            db.execute(select(Ticker).where(Ticker.ticker_code == ticker_code))
            .scalar_one_or_none()
        )
        if ticker is None:
            return []

        # latest cached date for this interval
        latest: datetime.date | None = (
            db.execute(
                select(func.max(ChartData.date)).where(
                    and_(ChartData.ticker_id == ticker.id, ChartData.interval == interval)
                )
            ).scalar_one()
        )

        today = datetime.now(timezone.utc).date()
        expected_next_date = (
            latest + timedelta(days=interval) if latest else today - timedelta(days=interval * 30)
        )

        if expected_next_date <= today:
            # fetch missing range
            fetched_rows = (
                _fetch_kospi(ticker_code, expected_next_date, today, interval)
                if ticker.market.upper() == "KOSPI"
                else _fetch_us(ticker_code, expected_next_date, today, interval)
            )

            # bulk insert
            for row in fetched_rows:
                db.add(
                    ChartData(
                        ticker_id=ticker.id,
                        date=row["date"],
                        interval=interval,
                        open=row["open"],
                        high=row["high"],
                        low=row["low"],
                        close=row["close"],
                        volume=row["volume"],
                        change=row["change"],
                    )
                )
            db.commit()

        # return last 30 records (or all)
        rows = (
            db.execute(
                select(ChartData)
                .where(and_(ChartData.ticker_id == ticker.id, ChartData.interval == interval))
                .order_by(ChartData.date)
            )
            .scalars()
            .all()
        )
        return [_row_to_dict(r) for r in rows]

# ──────────────────────────────────────────────────────────────────────────────
# helpers
# ──────────────────────────────────────────────────────────────────────────────

def _row_to_dict(r: ChartData) -> Dict:
    return {
        "date": r.date.isoformat(),
        "open": r.open,
        "high": r.high,
        "low": r.low,
        "close": r.close,
        "volume": r.volume,
        "change": r.change,
    }

def _fetch_us(ticker: str, 
              start: datetime.date, 
              end: datetime.date, 
              interval: int) -> List[Dict]:
    yf_interval = {1: "1d", 7: "1wk", 30: "1mo"}[interval]
    df = (
        yf.Ticker(ticker)
        .history(start=start - timedelta(days=interval*3), 
                 end=end + timedelta(days=1), 
                 interval=yf_interval)
        .round(2)
    )
    if df.empty:
        return []
    
    rows: List[Dict] = []
    prev_close = None
    
    for dt, row in df.iterrows():
        if(dt.date() < start):
            prev_close = row["Close"]
            continue
        
        change = (
            round((row["Close"] - prev_close) / prev_close, 4)
            if prev_close and prev_close != 0
            else 0
        )
        
        rows.append({
                "date": dt.date(),
                "open": row["Open"],
                "high": row["High"],
                "low": row["Low"],
                "close": row["Close"],
                "volume": int(row.get("Volume", 0)),
                "change": change,
        })
        prev_close = row["Close"]
        
    return rows

def _fetch_kospi(ticker: str,
                 start: datetime.date, 
                 end: datetime.date, 
                 interval: int) -> List[Dict]:
    # 1) 일간 데이터 먼저 수집
    df = fdr.DataReader(
        ticker, 
        start=start - timedelta(days=interval*3),
        end=end + timedelta(days=1)).round(2)
    if df.empty:
        return []

    # 2) 주간·월간이면 리샘플
    if interval != 1:
        rule = {7: "W-MON", 30: "MS"}[interval]
        df = (
            df.resample(rule, label="left", closed="left")
            .agg({
                "Open":  "first",
                "High":  "max",
                "Low":   "min",
                "Close": "last",
                "Volume":"sum"
            })
            .dropna()
        )

    # 3) 전일 종가 대비 change 계산
    rows: List[Dict] = []
    prev_close = None
    for dt, row in df.iterrows():
        if dt.date() < start:
            prev_close = row["Close"]
            continue

        change = (
            round((row["Close"] - prev_close) / prev_close, 4)
            if prev_close and prev_close != 0 else 0
        )

        rows.append({
            "date":   dt.date(),
            "open":   row["Open"],
            "high":   row["High"],
            "low":    row["Low"],
            "close":  row["Close"],
            "volume": int(row.get("Volume", 0)),
            "change": change,
        })
        prev_close = row["Close"]

    return rows
