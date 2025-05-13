# db/models/ticker.py
from sqlalchemy import Column, Integer, String
from ..session import Base

class Ticker(Base):
    __tablename__ = "ticker"

    id = Column(Integer, primary_key=True, index=True)
    ticker_code = Column(String(20), unique=True, nullable=False)
    company_name = Column(String(100))
    market = Column(String(10), nullable=False)
