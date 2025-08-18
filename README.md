# Stock Info API

This project provides a FastAPI-based backend to fetch stock-related information such as historical prices, recent news, prediction results, and XAI-based explanations. The backend is containerized using Docker and uses MySQL (RDS-ready) as its primary database.


## 1. Features

### 1.1. Search
**GET /search**

Autocomplete search for stock tickers and company names.

**Query Parameters**
- `keyword` (optional): partial match for ticker or name

```http
GET /search?keyword=apple
````

---

### 1.2. Stock Info APIs (Modularized)

#### `/stock-info/basic`

* Returns historical chart data and recent news
* **Query Parameters**:

  * `ticker`
  * `horizon` (1, 7, or 30)

```http
GET /stock-info/basic?ticker=AAPL&horizon=7
```

#### `/stock-info/pred`

* Returns predicted price data
* **Query Parameters**:

  * `ticker`
  * `horizon` (1, 7, or 30)

```http
GET /stock-info/pred?ticker=AAPL&horizon=7
```

#### `/stock-info/exp`

* Returns explanation (XAI tokens and scores)
* **Query Parameters**:

  * `ticker`
  * `horizon` (1, 7, or 30)

```http
GET /stock-info/exp?ticker=AAPL&horizon=7
```


## 2. Project Structure

```bash
backend/
├── app/
│   ├── main.py         # FastAPI app entrypoint
│   ├── crud/           # Logic layer: DB access for chart, prediction, news, explanation
│   ├── routers/
│   │   ├── stock.py    # /stock-info/* endpoints
│   │   └── search.py   # /search endpoint
│   ├── schemas.py      # Pydantic schemas
│   └── __init__.py
├── db/
│   ├── models/         # SQLAlchemy models: Ticker, ChartData, Prediction, News, Explanation
│   ├── session.py      # MySQL engine and session maker
│   └── init_db.py      # DB seeding or migration logic
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```


## 3. Setup & Run (Local)

### 3.0. Create `.env` file
```env
# External API for model inference (via ngrok or your own gateway)
NGROK_API_URL="https://<your-ngrok-or-api-url>.ngrok-free.app/"

# MySQL Database URL (RDS or local)
DATABASE_URL="mysql+pymysql://<username>:<password>@<host>:<port>/<database>"
```

### 3.1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate       # macOS/Linux
# or venv\Scripts\activate     # Windows
```

### 3.2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3.3. Start FastAPI App

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Visit:

* Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)


## 4. Docker Run (Docker Compose)

To build and run the backend with Docker Compose:

```bash
docker compose up -d --build
```

Make sure your .env file is created at the root level with proper MySQL and external inference settings.

### Example `.env` file
```env
# External API for model inference (via ngrok or your own gateway)
NGROK_API_URL="https://<your-ngrok-or-api-url>.ngrok-free.app/"

# MySQL Database URL (RDS or local)
DATABASE_URL="mysql+pymysql://<username>:<password>@<host>:<port>/<database>"
```

## 5. Contributor

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/DevJihun">
        <img src="https://github.com/DevJihun.png" width="60px;" alt="DevJihun"/>
        <br />
        <sub><b>Jihun Kim</b></sub>
      </a>
    </td>
  </tr>
</table>

