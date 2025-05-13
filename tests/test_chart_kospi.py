# tests/test_chart_kospi.py
import pandas as pd
from freezegun import freeze_time
from unittest.mock import patch
import pytest

from app.crud.chart import get_chart_data
from db.models.ticker import Ticker

CASES = [
    # interval, index_dates, expected_label, close_vals
    (1,  ["2025-05-14", "2025-05-15"], "2025-05-15", [70200, 70500]),
    (7,  ["2025-05-05", "2025-05-12"], "2025-05-12", [70200, 70500]),
    (30, ["2025-04-01", "2025-05-01"], "2025-05-01", [70200, 70500]),
]

@freeze_time("2025-05-15")
@patch("app.crud.chart.fdr.DataReader")
@pytest.mark.parametrize("interval, idx_dates, exp_date, closes", CASES)
def test_get_chart_data_kospi(mock_fdr, interval, idx_dates, exp_date, closes, db):
    """KOSPI용 get_chart_data가 1·7·30일 interval에서 모두 동작하는지 검증"""

    # ── 1) mock FDR 반환값 -----------------------------------------------------
    df = pd.DataFrame(
        {
            "Open":   [70000, 70200],
            "High":   [71000, 71500],
            "Low":    [69500, 70000],
            "Close":  closes,
            "Volume": [8_000_000, 7_500_000],
        },
        index=pd.to_datetime(idx_dates),
    )
    mock_fdr.return_value = df

    # ── 2) 테스트용 티커 시드 (중복 방지) --------------------------------------
    db.add(Ticker(ticker_code="005930", market="KOSPI"))
    db.commit()

    # ── 3) 함수 호출 & 검증 ----------------------------------------------------
    rows = get_chart_data("005930", interval=interval, session=db)

    assert len(rows) == 2
    assert rows[-1]["date"] == exp_date
    expected_change = round((closes[-1] - closes[-2]) / closes[-2], 4)
    assert rows[-1]["change"] == expected_change
