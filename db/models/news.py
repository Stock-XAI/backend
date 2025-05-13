# db/models/news.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from ..session import Base

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("ticker.id"), nullable=False)
    title = Column(String(200), nullable=False)
    summary = Column(Text)
    link = Column(String(200), nullable=False)
    pub_date = Column(DateTime, nullable=False)
    provider = Column(String(50))
