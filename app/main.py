# app/main.py
from fastapi import FastAPI
from .routers import stock, search
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(stock.router)    # /stock-info
app.include_router(search.router)   # /search 자동완성 API 추가

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Change to frontend URL in production (all origins for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Stock Prediction API",
        "status": "running",
        "endpoints": ["/stock-info", "/search"]
    }