# app/main.py
from fastapi import FastAPI
from .routers import stock

app = FastAPI()

app.include_router(stock.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Stock Prediction API",
        "status": "running",
        "endpoints": ["/stock-info"]
    }