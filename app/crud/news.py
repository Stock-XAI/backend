# app/crud/news.py
from __future__ import annotations

from typing import List, Dict, Optional
from contextlib import contextmanager
from datetime import datetime, timezone

import yfinance as yf
from dateutil import parser as date_parser
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from db.session import SessionLocal
from db.models.news import News
from db.models.ticker import Ticker


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


def get_recent_news(
    ticker_code: str,
    *,
    session: Session | None = None
) -> List[Dict]:
    """
    ticker_code에 대해 최근 10건 뉴스 반환
    - 헤드라인(pubDate) 비교로 새로운 뉴스 여부 판단
    - Ticker.market 정보로 US/KOSPI 구분하여 YF fetch (.KS suffix)
    - 신규 항목만 insert 후 최신 10건 반환
    """
    with _get_session(session) as db:
        # 1) Ticker 조회
        ticker: Ticker | None = db.execute(
            select(Ticker).where(Ticker.ticker_code == ticker_code)
        ).scalar_one_or_none()
        if not ticker:
            return []

        # 2) DB에 저장된 가장 최신 pub_date
        latest_db_date: datetime | None = db.execute(
            select(func.max(News.pub_date)).where(News.ticker_id == ticker.id)
        ).scalar_one()

        # 3) API 호출 준비: .KS suffix 처리
        fetch_code = (
            f"{ticker_code}.KS" if ticker.market.upper() == "KOSPI" else ticker_code
        )
        try:
            raw = yf.Ticker(fetch_code).news or []
        except Exception:
            raw = []

        # 4) 헤드라인 비교: raw에서 최대(pubDate) 구하기
        max_pub_dt: datetime | None = None
        for art in raw:
            pub_str = art.get("content", {}).get("pubDate", "")
            try:
                dt = date_parser.parse(pub_str)
                if dt.tzinfo:
                    dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
            except Exception:
                continue
            if max_pub_dt is None or dt > max_pub_dt:
                max_pub_dt = dt

        # 캐시 히트: API의 최신 뉴스가 DB 최신과 같거나 이전이면 DB에서 바로 반환
        print(max_pub_dt, latest_db_date)
        if max_pub_dt and latest_db_date and max_pub_dt <= latest_db_date:
            print("cahce")    
            rows = db.execute(
                select(News)
                .where(News.ticker_id == ticker.id)
                .order_by(News.pub_date.desc())
                .limit(10)
            ).scalars().all()
            return [
                {
                    "title":    n.title,
                    "summary":  n.summary,
                    "link":     n.link,
                    "pubDate":  n.pub_date.isoformat(),
                    "provider": n.provider
                }
                for n in rows
            ]

        # 5) 전체 뉴스 파싱 및 DB에 없는 항목 필터
        new_items: list[tuple[Dict, datetime]] = []
        for art in raw:
            content = art.get("content", {})
            title = content.get("title")
            link = content.get("canonicalUrl", {}).get("url")
            pub_str = content.get("pubDate", "")
            provider = content.get("provider", {}).get("displayName", "")
            if not (title and link):
                continue

            try:
                pub_dt = date_parser.parse(pub_str)
                if pub_dt.tzinfo:
                    pub_dt = pub_dt.astimezone(timezone.utc).replace(tzinfo=None)
            except Exception:
                continue

            if not latest_db_date or pub_dt > latest_db_date:
                new_items.append((
                    {
                        "title":   title,
                        "summary": content.get("summary", ""),
                        "link":    link,
                        "pubDate": pub_dt,
                        "provider": provider
                    },
                    pub_dt
                ))

        # 6) 신규 뉴스 bulk insert 후 커밋
        for item, pub_dt in new_items:
            db.add(News(
                ticker_id=ticker.id,
                title=item["title"],
                summary=item["summary"],
                link=item["link"],
                pub_date=pub_dt,
                provider=item["provider"]
            ))
        if new_items:
            db.commit()

        # 7) 최신 10건 조회 및 반환
        rows = db.execute(
            select(News)
            .where(News.ticker_id == ticker.id)
            .order_by(News.pub_date.desc())
            .limit(10)
        ).scalars().all()
        return [
            {
                "title":    n.title,
                "summary":  n.summary,
                "link":     n.link,
                "pubDate":  n.pub_date.isoformat(),
                "provider": n.provider
            }
            for n in rows
        ]
