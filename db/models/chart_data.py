# db/models/chart_data.py
from sqlalchemy import Column, Integer, Float, Date, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from ..session import Base

class ChartData(Base):
    __tablename__ = "chart_data"

    ticker_id = Column(Integer, ForeignKey("ticker.id"), primary_key=True)
    date = Column(Date, primary_key=True)
    interval = Column(Integer, primary_key=True)  # 1, 7, 30
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)
    change = Column(Float)
