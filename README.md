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

Example Request:
```
GET /stock-info?ticker=AAPL&horizon=7&includeNews=true&includeXAI=true
```


## 2. Project Structure

```
myproject/
├── app/
│   ├── main.py            # FastAPI entrypoint (app 객체, 라우터 등록)
│   ├── routers/
│   │   └── stock.py       # /stock-info 라우터 정의
│   ├── database.py        # MongoDB 연결 (pymongo)
│   ├── crud.py            # 예측/뉴스/DB 관련 로직 모음 (선택)
│   ├── schemas.py         # Pydantic 데이터 모델 (Request/Response)
│   └── __init__.py
├── requirements.txt       # Python 패키지 목록
└── Dockerfile             # Docker 빌드 설정
```

- app/main.py: FastAPI 애플리케이션을 생성하고, 라우터들을 등록합니다.
- app/routers/stock.py: `/stock-info` 라우트를 정의합니다.
- app/database.py: MongoDB에 연결하는 클라이언트를 설정합니다. pymongo 기반입니다.
- app/crud.py: 예측, 뉴스, 해석 결과를 MongoDB에서 가져오거나 가공하는 로직이 들어갑니다. (현재 Mock data 사용)
- app/schemas.py: 요청 및 응답의 데이터 구조를 정의합니다 (Pydantic 사용).


## 3. Setup & Run (Local)

### 3.1. Create a Python virtual environment (optional, but recommended)

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
- Test endpoint: http://localhost:8000/stock-info?ticker=AAPL&horizon=7&includeNews=true&includeXAI=true


## 4. Docker Build & Run

### 4.1. Build Docker Image

```bash
docker build -t stockinfo:latest .
```

### 4.2. Run the Container

```bash
docker run -d -p 8000:8000 --name stockinfo-app stockinfo:latest
```

### 4.3. Verify

```bash
curl "http://localhost:8000/stock-info?ticker=AAPL&horizon=7&includeNews=true&includeXAI=true"
```


## 5. Contributor

TBD
