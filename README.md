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
 ┗ main.py           # FastAPI main source
```
TBD

- **main.py**: Core FastAPI application


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
uvicorn main:app --host 0.0.0.0 --port 8000
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
