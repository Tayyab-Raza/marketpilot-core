# REQUIREMENTS — MarketPilot AI

## 1. Functional requirements

### FR-001 Instrument registry
The system shall maintain a canonical instrument registry independent of any provider.

Canonical example:
```yaml
instrument_id: NSE_INDEX_NIFTY50
asset_class: index
exchange: NSE
currency: INR
timezone: Asia/Kolkata
provider_symbols:
  upstox: "NSE_INDEX|Nifty 50"
  marketstack: null
```

### FR-002 Provider abstraction
All data access must pass through provider adapters.

Required interface:
```text
get_quote()
get_eod()
get_historical_candles()
get_intraday_candles()
get_option_contracts()
get_option_chain()
get_open_interest()
get_volatility_index()
get_ipo_list()
get_ipo_details()
```

Unsupported methods must return a typed `CapabilityNotSupported` error.

### FR-003 Marketstack adapter
Support:
- EOD
- historical EOD
- ticker/exchange metadata

The application must not assume Marketstack supports Indian F&O data.

### FR-004 Upstox adapter
Support, subject to user authorization/API availability:
- full quote
- historical candles
- intraday candles
- WebSocket market stream
- option contracts
- option chain
- OI
- Greeks
- India VIX
- IPO endpoints

### FR-005 NSE reference ingestion
Support scheduled ingestion from official NSE-published files/reports where legally and technically permitted.

### FR-006 Forex adapter
Define generic adapter now; implement Twelve Data later.

### FR-007 Daily ingestion
At minimum:
- previous 250+ sessions of daily data where available
- latest completed session
- derivatives snapshots
- India VIX
- market breadth/context

### FR-008 Intraday history
For timing models, ingest 1m/5m/15m historical bars.

Without intraday history, the UI must label time predictions:
`UNAVAILABLE — insufficient intraday data`.

### FR-009 Data normalization
Normalize:
- timestamps to UTC internally
- display timezone Asia/Kolkata
- prices Decimal/NUMERIC
- volume integer
- OI integer
- percentages decimal fraction

### FR-010 Feature engine
Compute:
- daily return
- overnight gap
- true range
- ATR 14
- realized volatility
- SMA/EMA 5/10/20/50/100/200
- RSI 14
- MACD
- ADX
- Bollinger Bands
- rolling high/low
- pivot points
- VWAP where intraday data exists
- gap statistics
- opening-range statistics
- historical time-of-day behavior

### FR-011 Derivatives feature engine
Compute:
- futures basis
- futures OI change
- long build-up
- short build-up
- long unwinding
- short covering
- PCR by OI
- PCR by volume
- call/put OI concentrations
- change-in-OI concentrations
- IV surface summary
- IV percentile
- ATM straddle implied move
- delta-weighted exposure proxy
- gamma concentration proxy

### FR-012 Regime classifier
Output one regime plus probabilities:
- bullish trend
- bearish trend
- range
- volatile bullish
- volatile bearish
- event/uncertain

### FR-013 Next-day forecast
Generate:
- P(up)
- P(down)
- P(range)
- expected close return
- expected high
- expected low
- expected range
- uncertainty interval

### FR-014 Scenario engine
Always generate at least:
- bullish scenario
- bearish scenario
- neutral/no-trade scenario

### FR-015 Strategy generator
Each executable-looking setup must include:
- direction
- entry zone
- confirmation
- stop
- targets
- risk/reward
- invalidation
- confidence
- data timestamp

### FR-016 Time-window prediction
Estimate:
- likely first test of entry zone
- likely first test of T1/T2

Rules:
- output intervals, not exact guaranteed timestamps
- include probability
- include sample size
- suppress prediction below minimum sample threshold

### FR-017 Multi-horizon forecasts
Produce:
- 1 week
- 1 month
- 3 months
- 6 months
- 1 year

### FR-018 Backtest engine
Backtest every strategy template using walk-forward validation.

Minimum outputs:
- trades
- win rate
- expectancy
- profit factor
- max drawdown
- Sharpe-like metric
- MAE
- MFE
- target hit probability
- stop hit probability
- calibration

### FR-019 Paper-trade journal
Persist each generated plan before the next session so results cannot be rewritten after the fact.

### FR-020 IPO module
Retrieve:
- issue name
- open/close dates
- listing date
- price band
- lot size
- issue size
- fresh issue/OFS
- subscription figures
- business/financial metrics when available
- peer valuation
- risk flags

### FR-021 IPO recommendation
Output:
- APPLY
- WATCH
- AVOID
- INSUFFICIENT DATA

Every output must provide reasons and confidence.

### FR-022 Explainability
Every forecast must show top contributing factors.

### FR-023 Alerts
Future:
- EOD report ready
- level reached
- setup invalidated
- unusual IV/OI activity
- IPO status changed

## 2. Non-functional requirements

### NFR-001 Reliability
No strategy generation on incomplete or stale data.

### NFR-002 Idempotency
Re-ingesting the same provider payload must not create duplicate candles.

### NFR-003 Traceability
Every derived result must store:
- source provider
- source timestamp
- code/model version
- feature version

### NFR-004 Security
- secrets only in environment/secret manager
- never store broker password
- OAuth tokens encrypted at rest

### NFR-005 Performance
EOD report for one instrument should complete in seconds after data availability.

### NFR-006 Scalability
Architecture must support thousands of instruments without changing domain schemas.

### NFR-007 Testing
Minimum:
- unit tests
- provider contract tests
- data-quality tests
- feature tests
- backtest reproducibility tests

### NFR-008 Observability
Log:
- provider latency
- rate limits
- ingestion failures
- missing candles
- model drift
- forecast calibration

## 3. Data-quality gates
Do not forecast if:
- latest session is missing
- OHLC impossible (low > high, etc.)
- duplicate timestamps unresolved
- option chain expiry inconsistent
- stale quote beyond configured threshold

## 4. Recommended MVP stack
- Python 3.12+
- FastAPI
- PostgreSQL
- TimescaleDB extension optional
- Redis optional
- Celery/ARQ/APScheduler for jobs
- pandas/polars
- NumPy
- scikit-learn
- LightGBM/XGBoost optional
- vectorbt/backtesting.py/custom engine
- Pydantic
- React/Next.js for UI
- Docker Compose

## 5. Risk requirements
- default risk per paper trade configurable, suggested 0.25–1.0%
- no averaging-down recommendation by default
- max daily loss limit
- no-trade recommendation permitted and encouraged
- confidence threshold required before a setup is displayed as primary
