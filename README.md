# Stock Info API

This project provides a simple FastAPI-based backend to fetch stock-related information (mock data in this example), such as past prices, recent news, and a basic prediction with XAI explanation. The API is containerized with Docker for easy deployment.


## 1. Features

1. **Landing Page**: (Front-end perspective, not an API) – A simple page with a search bar for the stock ticker.  
2. **GET /stock-info**:  
  - Fetches chart data, news, prediction result, and explanation in one go, based on query params:
    - `ticker` (required)
    - `horizon` (optional, default 7)
    - `includeNews` (optional, boolean, default true)
    - `includeXAI` (optional, boolean, default true)
  ```
  GET /stock-info?ticker=AAPL&horizon=7&includeNews=true&includeXAI=true
  ```
3. GET /search
  - Autocomplete for stock tickers and company names
  - Query parameters:
    - keyword (required): partial string for matching ticker or name
  ```http
  GET /search?keyword=apple
  ```

## 2. Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI entrypoint and router registration
│   ├── database.py          # MongoDB connection via pymongo
│   ├── crud.py              # Logic for fetching mock data (prediction, news)
│   ├── schemas.py           # Pydantic models for API request/response
│   ├── routers/
│   │   ├── stock.py         # /stock-info endpoint
│   │   └── search.py        # /search endpoint
│   └── __init__.py
├── scripts/
│   └── seed_us_stocks.py    # Seed S&P500 + NASDAQ100 tickers to MongoDB
├── requirements.txt         # Python dependencies
├── Dockerfile
└── docker-compose.yml
```

## 3. Setup & Run (Local)

### 3.1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate       # (macOS/Linux)
# or venv\Scripts\activate     # (Windows)
```

### 3.2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3.3. Run FastAPI with Uvicorn

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

- The server should be available at http://localhost:8000
- Swagger: http://localhost:8000/docs

## 4. Docker Run (Docker Compose)

```bash
docker-compose up -d --build
```

## 5. Contributor

TBD
