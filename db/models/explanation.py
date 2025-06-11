# db/models/explaination.py
from sqlalchemy import Column, Integer, Date, ForeignKey, Text, UniqueConstraint
import json
from ..session import Base

class Explanation(Base):
    __tablename__ = "explanation"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("ticker.id"), nullable=False)
    predicted_date = Column(Date, nullable=False)
    horizon_days = Column(Integer, nullable=False)
    token = Column(Text)
    token_score = Column(Text)

    __table_args__ = (
        UniqueConstraint("ticker_id", "predicted_date", "horizon_days", name="uq_explanation_main"),
    )

    def set_token(self, token_list):
        self.token = json.dumps(token_list)

    def get_token(self):
        return json.loads(self.token)

    def set_token_score(self, score_list):
        self.token_score = json.dumps(score_list)

    def get_token_score(self):
        return json.loads(self.token_score)

