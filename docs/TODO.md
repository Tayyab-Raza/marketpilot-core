# TODO — Fastest Execution Plan

## Goal
Ship a trustworthy NIFTY 50 EOD + next-day strategy MVP first. Do not begin with every asset class.

---

## Day 1 — Foundation
### 1. Repository
- [ ] initialize Git
- [ ] Python 3.12 environment
- [ ] FastAPI
- [ ] PostgreSQL
- [ ] Docker Compose
- [ ] `.env.example`
- [ ] lint/test configuration

### 2. Provider accounts
- [ ] create Marketstack key
- [ ] create/configure Upstox developer app
- [ ] verify NIFTY 50 instrument key
- [ ] test quote endpoint
- [ ] test historical V3 endpoint
- [ ] test option-contract endpoint
- [ ] test option-chain endpoint
- [ ] test OI endpoint
- [ ] test IPO endpoint

### 3. Canonical instruments
- [ ] add NIFTY 50
- [ ] add India VIX
- [ ] add NIFTY futures mapping logic

**Exit criterion:** a script returns today's NIFTY quote and historical candles.

---

## Day 2 — Database + ingestion
- [ ] create migrations
- [ ] `instruments`
- [ ] `provider_instruments`
- [ ] `candles`
- [ ] derivative tables
- [ ] raw provider payload audit table
- [ ] implement Upstox adapter
- [ ] implement Marketstack EOD adapter
- [ ] implement data-quality checks

**Exit criterion:** latest + historical NIFTY data persists idempotently.

---

## Day 3 — Technical engine
- [ ] ATR
- [ ] SMA/EMA
- [ ] RSI
- [ ] MACD
- [ ] ADX
- [ ] Bollinger
- [ ] rolling support/resistance
- [ ] expected range baseline
- [ ] regime baseline

**Exit criterion:** deterministic market summary JSON.

---

## Day 4 — F&O engine
- [ ] expiry resolver
- [ ] option-chain ingestion
- [ ] PCR OI
- [ ] PCR volume
- [ ] ATM IV
- [ ] call/put OI walls
- [ ] change-OI walls
- [ ] implied move from ATM straddle
- [ ] futures OI/basis
- [ ] Greeks storage when available

**Exit criterion:** F&O summary JSON for current expiry.

---

## Day 5 — Forecast v1
Start simple.

- [ ] baseline historical conditional forecast
- [ ] logistic classifier
- [ ] quantile range model
- [ ] walk-forward split
- [ ] calibration metrics
- [ ] model registry

Do NOT add deep learning yet.

**Exit criterion:** next-day P(up/down/range) + high/low quantiles.

---

## Day 6 — Strategy + backtest
- [ ] bull scenario
- [ ] bear scenario
- [ ] no-trade scenario
- [ ] entry zone rules
- [ ] ATR/structure stop
- [ ] target logic
- [ ] R:R filter
- [ ] immutable daily plan
- [ ] historical evaluation
- [ ] MAE/MFE

**Exit criterion:** every forecast produces a reproducible trade plan or NO TRADE.

---

## Day 7 — Timing model + UI
- [ ] ingest enough historical intraday data
- [ ] first-touch time buckets
- [ ] probability by time bucket
- [ ] suppress low-sample forecasts
- [ ] build dashboard
- [ ] daily summary
- [ ] F&O panel
- [ ] strategy card
- [ ] confidence/calibration
- [ ] data-status panel

**Exit criterion:** usable browser-based NIFTY daily research dashboard.

---

# Week 2 — Validation
- [ ] replay minimum 1–3 years daily history
- [ ] use intraday history available from provider
- [ ] transaction cost assumptions
- [ ] slippage assumptions
- [ ] expiry-day segmentation
- [ ] gap-day segmentation
- [ ] VIX-regime segmentation
- [ ] audit data leakage
- [ ] confidence calibration

**Do not trade live based on the model until paper results are stable.**

---

# Week 3 — Paper trading
Every day:
- [ ] generate plan after EOD
- [ ] hash/freeze plan
- [ ] next day evaluate
- [ ] record first entry touch
- [ ] stop/target sequence
- [ ] timing accuracy
- [ ] reasons for failure
- [ ] calibration update

Suggested minimum before meaningful conclusions:
- 60–100 independent daily forecasts
- more for individual strategy subtypes

---

# Week 4 — NIFTY production hardening
- [ ] provider retries
- [ ] stale-data alerts
- [ ] market holiday calendar
- [ ] WebSocket reconciliation
- [ ] observability
- [ ] secrets manager
- [ ] backups
- [ ] test suite
- [ ] CI/CD

---

# Phase 2 — Intraday live assistant
- [ ] Upstox market stream V3
- [ ] 1m bar builder
- [ ] 5m/15m aggregation
- [ ] live VWAP
- [ ] opening range
- [ ] live OI/IV changes
- [ ] setup activation alerts
- [ ] setup invalidation alerts

---

# Phase 3 — Expand Indian F&O
Do not hardcode NIFTY logic.

- [ ] BANKNIFTY
- [ ] FINNIFTY if applicable
- [ ] NSE F&O stocks
- [ ] automatic contract resolver
- [ ] per-symbol model calibration

---

# Phase 4 — Forex
- [ ] implement Twelve Data adapter
- [ ] canonical FX instruments
- [ ] 24x5 sessions
- [ ] timezone/session features
- [ ] FX-specific spread/slippage
- [ ] macro calendar integration

---

# Phase 5 — IPO agent
- [ ] ingest Upstox IPO list/details
- [ ] NSE/BSE/SEBI validation
- [ ] financial statement ingestion
- [ ] peer mapping
- [ ] valuation model
- [ ] subscription tracking
- [ ] IPO scoring
- [ ] post-listing outcome evaluation

---

# Priority matrix

## P0 — must have
- reliable NIFTY data
- F&O chain/OI
- data-quality gate
- next-day range/probability
- entry/stop/targets
- no-trade state
- immutable paper record
- backtest

## P1
- timing probability
- live feed
- Greeks
- multi-horizon models
- dashboard

## P2
- IPO
- forex
- more NSE stocks

## P3
- automatic broker execution

---

# Definition of Done for MVP
The MVP is done only when:
- [ ] it fetches NIFTY data automatically
- [ ] it detects stale/missing data
- [ ] it produces today's complete summary
- [ ] it produces tomorrow's probabilistic range
- [ ] it produces bull, bear, no-trade scenarios
- [ ] it provides entry/stop/targets only under defined rules
- [ ] it provides timing ranges only when intraday evidence exists
- [ ] it saves the forecast before the next session
- [ ] it scores the result after the session
- [ ] performance metrics are visible
- [ ] a losing/no-trade forecast is allowed
- [ ] no UI uses the words "guaranteed" or "perfect prediction"
