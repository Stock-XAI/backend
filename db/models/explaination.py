# db/models/explaination.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Text
import json
from ..session import Base

class Explaination(Base):
    __tablename__ = "explaination"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("ticker.id"), nullable=False)
    predicted_date = Column(Date, nullable=False)
    horizon_days = Column(Integer, nullable=False)
    token = Column(Text)       # JSON 직렬화된 string
    token_score = Column(Text) # JSON 직렬화된 string

    def set_token(self, token_list):
        self.token = json.dumps(token_list)

    def get_token(self):
        return json.loads(self.token)

    def set_token_score(self, score_list):
        self.token_score = json.dumps(score_list)

    def get_token_score(self):
        return json.loads(self.token_score)

