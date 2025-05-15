# tests/test_chart_us.py
import pandas as pd
from freezegun import freeze_time
from unittest.mock import patch
import pytest

from app.crud.chart import get_chart_data
from db.models.ticker import Ticker

CASES = [
    # interval, index_dates, expected_label, close_vals
    (1,  ["2025-05-14", "2025-05-15"], "2025-05-15", [102, 101]),
    (7,  ["2025-05-05", "2025-05-12"], "2025-05-12", [110, 115]),
    (30, ["2025-04-01", "2025-05-01"], "2025-05-01", [120, 118]),
]

@freeze_time("2025-05-15")
@patch("app.crud.chart.yf.Ticker")
@pytest.mark.parametrize("interval, idx_dates, exp_date, closes", CASES)
def test_get_chart_data_us(mock_yf, interval, idx_dates, exp_date, closes, db):
    """US용 get_chart_data가 1·7·30일 interval에서 모두 동작하는지 검증"""
    
    # ── 1) mock yfinance 반환값 -----------------------------------------------------
    df = pd.DataFrame(
        {
            "Open":  [100, 102],
            "High":  [105, 106],
            "Low":   [99,  100],
            "Close": closes,
            "Volume": [1_000_000, 900_000],
        },
        index=pd.to_datetime(idx_dates),
    )
    mock_yf.return_value.history.return_value = df

    # ── 2) 테스트용 티커 시드 (중복 방지) --------------------------------------
    db.add(Ticker(ticker_code="AAPL", market="US"))
    db.commit()

    # ── 3) 함수 호출 & 검증 ----------------------------------------------------
    rows = get_chart_data("AAPL", interval=interval, session=db)

    assert len(rows) == 2
    assert rows[-1]["date"] == exp_date
    expected_change = round((closes[-1] - closes[-2]) / closes[-2], 4)
    assert rows[-1]["change"] == expected_change
