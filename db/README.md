## Database Structure

The Stock-XAI backend uses a MySQL database to manage core financial data including stock tickers, price history, prediction results, news, and XAI explanations. Below is the detailed schema design.

### Schema Overview

```sql
Table Ticker {
  id int [pk, increment]
  ticker_code varchar [unique, not null]  // e.g., "AAPL", "005930.KS"
  company_name varchar
  market varchar [not null]               // e.g., "US", "KOSPI"
}
```

* **Description**: Master table for stock information including ticker code, company name, and market type.

```sql
Table ChartData {
  ticker_id int [ref: > Ticker.id, not null]
  date date [not null]
  interval int [not null]                 // 1 = daily, 7 = weekly, 30 = monthly
  open float
  high float
  low float
  close float
  volume bigint
  change float

  Indexes {
    (ticker_id, date, interval) [pk]
  }
}
```

* **Description**: Stores OHLCV chart data at different intervals. The primary key is a composite of `ticker_id`, `date`, and `interval`.

```sql
Table Prediction {
  id int [pk, increment]
  ticker_id int [ref: > Ticker.id, not null]
  predicted_date date [not null]
  horizon_days int [not null]             // e.g., 1, 7, 30
  prediction_result float

  Indexes {
    (ticker_id, predicted_date, horizon_days) [unique]
  }
}
```

* **Description**: Contains stock price prediction results for a given date and forecast horizon. Each record is uniquely identified by `ticker_id + date + horizon`.


```sql
Table News {
  id int [pk, increment]
  ticker_id int [ref: > Ticker.id, not null]
  title varchar [not null]
  summary text
  link varchar [not null]
  pub_date datetime [not null]
  provider varchar

  Indexes {
    (ticker_id, title, pub_date)
  }
}
```

* **Description**: Stores recent news articles related to each stock. Deduplicated using a compound index of `ticker_id`, `title`, and `pub_date`.


```sql
Table Explanation {
  id int [pk, increment]
  ticker_id int [ref: > Ticker.id, not null]
  predicted_date date [not null]
  horizon_days int [not null]
  token text                        // JSON-serialized list of tokens
  token_score text                  // JSON-serialized list of scores

  Indexes {
    (ticker_id, predicted_date, horizon_days) [unique]
  }
}
```

* **Description**: Stores XAI explanation results for each prediction. The `token` and `token_score` fields contain JSON-formatted arrays that align token importance with model predictions.


## Relational Structure Summary

* `Ticker` is the central table referenced by all others.
* `ChartData`, `Prediction`, `News`, and `Explanation` are linked to tickers via `ticker_id`.
* `ChartData` uses a composite primary key (`ticker_id + date + interval`) for optimized historical lookup.
* `Prediction` and `Explanation` use a unique constraint on `ticker_id + predicted_date + horizon_days` to avoid duplicates.
