# db/models/prediction.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from ..session import Base

class Prediction(Base):
    __tablename__ = "prediction"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("ticker.id"), nullable=False)
    predicted_date = Column(Date, nullable=False)
    horizon_days = Column(Integer, nullable=False)
    prediction_result = Column(String(30))
