## DB structure

```sql
Table Ticker {
  id int [pk, increment]
  ticker_code varchar [unique, not null] // "AAPL", "005930.KS"
  company_name varchar
  market varchar [not null]              // "US", "KOSPI"
}

Table ChartData {
  ticker_id int [ref: > Ticker.id, not null]
  date date [not null]
  interval int [not null] // 단위: days (1 = 일간, 7 = 주간, 30 = 월간)
  open float
  high float
  low  float
  close float
  volume bigint
  change float

  Indexes {
    (ticker_id, date, interval) [pk]
  }
}

Table Prediction {
  id int [pk, increment]
  ticker_id int [ref: > Ticker.id, not null]
  predicted_date date [not null]
  horizon_days int [not null]
  prediction_result varchar

  Indexes {
    (ticker_id, predicted_date, horizon_days) [unique]
  }
}

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