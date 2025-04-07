# app/crud.py
from pymongo.collection import Collection
from .schemas import StockCreate, StockUpdate
from bson.objectid import ObjectId
from typing import Optional

def create_stock(collection: Collection, stock_in: StockCreate):
    doc = stock_in.dict()
    result = collection.insert_one(doc)
    return str(result.inserted_id)

def get_stock(collection: Collection, ticker: str):
    doc = collection.find_one({"ticker": ticker})
    return doc

def update_stock(collection: Collection, ticker: str, stock_in: StockUpdate):
    update_data = {k: v for k, v in stock_in.dict(exclude_unset=True).items() if v is not None}
    result = collection.update_one({"ticker": ticker}, {"$set": update_data})
    return result.modified_count

def delete_stock(collection: Collection, ticker: str):
    result = collection.delete_one({"ticker": ticker})
    return result.deleted_count
