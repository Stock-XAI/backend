# app/crud/explanation.py
from typing import Dict
from sqlalchemy.orm import Session

from db.session import SessionLocal

from app.crud.utils import get_session

def generate_explanation(
    ticker_code: str,
    horizon: int,
    session: Session | None = None
) -> Dict[str, object]:
    """
    주어진 ticker_code와 horizon_days에 대한 XAI 해석 결과를 반환합니다.
    세션이 필요할 경우, DB에서 추가 정보를 조회할 때 사용 가능합니다.
    현재는 SHAP/LIME 연동 전 placeholder 함수입니다.

    반환 형식:
        {
            "why": str,          # 설명 텍스트
            "shapValues": List[float],
            "features": List[str]
        }
    """
    # 필요 시 세션 주입
    with get_session(session) as db:
        # TODO: SHAP 또는 LIME 기반 실제 설명 로직 구현
        pass

    # Placeholder 반환
    return {
        "why": "주가 상승 요인은 거래량 증가 및 단기 이동평균 우위",
        "shapValues": [0.12, -0.07],
        "features": ["MA_5", "Volume"]
    }