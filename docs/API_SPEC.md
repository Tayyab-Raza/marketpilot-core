# API_SPEC — MarketPilot AI

## Base
`/api/v1`

All dates ISO-8601.  
All timestamps ISO-8601 with timezone.

## 1. Health

### GET `/health`
Response:
```json
{
  "status": "ok",
  "db": "ok",
  "providers": {
    "upstox": "ok",
    "marketstack": "configured"
  }
}
```

## 2. Instruments

### GET `/instruments`
Filters:
- asset_class
- exchange
- query

### GET `/instruments/{instrument_id}`

## 3. Market data

### GET `/market/{instrument_id}/quote`

### GET `/market/{instrument_id}/candles`
Query:
```text
interval=1d
from=2026-01-01
to=2026-10-05
provider=auto
```

### GET `/market/{instrument_id}/summary`
Response:
```json
{
  "instrument": "NSE_INDEX_NIFTY50",
  "session": "2026-10-05",
  "open": 0,
  "high": 0,
  "low": 0,
  "close": 0,
  "previous_close": 0,
  "change_pct": 0,
  "range_pct": 0,
  "atr14": 0,
  "rsi14": 0,
  "adx14": 0,
  "regime": "RANGE",
  "data_as_of": "..."
}
```

## 4. F&O

### GET `/fno/{instrument_id}/expiries`

### GET `/fno/{instrument_id}/option-chain`
Query:
```text
expiry=current_week
```

### GET `/fno/{instrument_id}/oi-analysis`
Response:
```json
{
  "pcr_oi": 0.91,
  "pcr_volume": 0.87,
  "call_wall": 0,
  "put_wall": 0,
  "atm_iv": 0,
  "implied_move": 0,
  "summary": "..."
}
```

### GET `/fno/{instrument_id}/futures-analysis`

## 5. Forecasts

### POST `/forecast/{instrument_id}/run`
Body:
```json
{
  "as_of": "latest",
  "horizons": ["1d", "1w", "1m", "3m", "6m", "1y"],
  "force": false
}
```

### GET `/forecast/{instrument_id}/latest`

Response:
```json
{
  "as_of": "...",
  "next_session": {
    "p_up": 0.62,
    "p_down": 0.25,
    "p_range": 0.13,
    "expected_low": 0,
    "expected_high": 0,
    "confidence": 0.68
  },
  "horizons": []
}
```

## 6. Strategy

### POST `/strategy/{instrument_id}/generate`

Response:
```json
{
  "target_session": "YYYY-MM-DD",
  "bias": "BULLISH",
  "confidence": 0.68,
  "regime": "BULLISH_TREND",
  "expected_range": {
    "low": 0,
    "high": 0
  },
  "primary_setup": {
    "direction": "LONG",
    "entry_zone": [0, 0],
    "confirmation": "...",
    "stop": 0,
    "targets": [0, 0, 0],
    "entry_time_window": {
      "from": "09:45",
      "to": "11:15",
      "probability": 0.61
    },
    "target_windows": [],
    "invalidation": "..."
  },
  "bear_case": {},
  "no_trade_conditions": [],
  "disclaimer": "Probabilistic research output; not a guaranteed forecast."
}
```

### GET `/strategy/{instrument_id}/latest`

### GET `/strategy/{instrument_id}/history`

## 7. Backtest

### POST `/backtests`
Body:
```json
{
  "instrument_id": "NSE_INDEX_NIFTY50",
  "strategy_version": "v1",
  "from": "2022-01-01",
  "to": "2026-09-30"
}
```

### GET `/backtests/{id}`

## 8. Performance

### GET `/performance/forecast`
Returns:
- calibration
- accuracy
- Brier score
- quantile coverage

### GET `/performance/strategy`
Returns:
- expectancy
- max drawdown
- hit rate
- profit factor
- MAE/MFE

## 9. IPO

### GET `/ipos`
Query:
```text
status=upcoming|open|closed|listed
issue_type=regular|sme
```

### GET `/ipos/{id}`

### POST `/ipos/{id}/analyse`

Response:
```json
{
  "score": 74,
  "recommendation": "CONSIDER",
  "confidence": 0.72,
  "valuation": {},
  "financial_quality": {},
  "issue_quality": {},
  "subscription": {},
  "risks": [],
  "reasons": []
}
```

## 10. Provider status

### GET `/providers`
Shows capabilities.

Example:
```json
[
  {
    "name": "marketstack",
    "capabilities": ["eod", "historical_eod"]
  },
  {
    "name": "upstox",
    "capabilities": [
      "quote",
      "historical",
      "intraday",
      "stream",
      "option_chain",
      "oi",
      "ipo"
    ]
  }
]
```

## 11. Admin ingestion

### POST `/admin/ingestion/eod`
Protected.

### POST `/admin/reconcile/{instrument_id}`
Protected.

## 12. Error model
```json
{
  "error": {
    "code": "STALE_DATA",
    "message": "Latest completed market session is unavailable.",
    "details": {}
  }
}
```

Codes:
- `PROVIDER_ERROR`
- `RATE_LIMITED`
- `CAPABILITY_NOT_SUPPORTED`
- `STALE_DATA`
- `DATA_QUALITY_FAILED`
- `INSUFFICIENT_HISTORY`
- `MODEL_UNAVAILABLE`
- `AUTH_REQUIRED`
