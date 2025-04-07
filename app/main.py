# app/main.py
from fastapi import FastAPI
from .routers import stock, search

app = FastAPI()

app.include_router(stock.router)    # /stock-info
app.include_router(search.router)   # /search 자동완성 API 추가

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Stock Prediction API",
        "status": "running",
        "endpoints": ["/stock-info", "/search"]
    }