# app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

# PyMongo에서 _id는 ObjectId를 사용하므로, 다음과 같은 별도 헬퍼가 필요할 수도 있음
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

# MongoDB 문서용 기본 스키마
class StockBase(BaseModel):
    ticker: str = Field(...)
    name: str = Field(...)
    price: float = Field(...)

class StockCreate(StockBase):
    pass

class StockUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]

class StockOut(StockBase):
    # MongoDB _id 필드를 표시하고 싶다면
    id: Optional[str] = Field(alias="_id")

    class Config:
        # _id를 str로 serialize하기 위한 설정
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
