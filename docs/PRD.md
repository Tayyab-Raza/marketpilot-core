# PRD — AI Market Intelligence & F&O Strategy Agent

## 1. Product name
**MarketPilot AI** (working name)

## 2. Product objective
Build a modular AI-assisted market analysis system that ingests historical and current market data, produces a structured next-session trading plan for **NSE NIFTY 50**, and later expands to:
- NSE equities
- NSE index/stock futures and options
- Forex
- Global indices
- Commodities
- Indian IPO analysis

The product is an **analysis and decision-support system**, not a guaranteed prediction engine.

## 3. Primary user outcome
After market close, the user opens one dashboard and gets:

1. Today's NIFTY 50 summary
2. Trend and market-regime analysis
3. Important support/resistance levels
4. F&O positioning and option-chain interpretation
5. Tomorrow's bullish / bearish / neutral scenarios
6. Entry zone
7. Stop-loss
8. Target 1 / Target 2 / Target 3
9. Suggested instrument type (spot reference / futures / CE / PE)
10. Estimated probability/confidence
11. Estimated time window for an entry setup to become valid
12. Estimated time window for targets to be tested
13. Invalidation conditions
14. 1-week / 1-month / 3-month / 6-month / 1-year directional outlook
15. Backtest statistics for the same setup
16. IPO watchlist with Apply / Avoid / Watch classification

## 4. Important product constraint
The product MUST NOT state that tomorrow's exact price or exact time is certain.

Instead of:
> Buy at 24,500 at 10:17 AM and sell at 24,720 at 1:42 PM.

It should output:
> Entry zone: 24,480–24,520, valid only after confirmation.  
> Highest-probability setup window: 09:45–11:15 IST.  
> Target-1 test window: 11:00–14:00 IST.  
> Confidence: 68%.  
> Invalidation: sustained 15-minute close below 24,390.

Time forecasts must be expressed as **probability windows**, derived from historical intraday path distributions.

## 5. MVP scope

### Instrument
- NSE NIFTY 50 index
- NIFTY futures
- NIFTY options around ATM and configurable strike range

### Analysis frequency
- Primary: EOD after market close
- Optional Phase 2: intraday refresh every 1–5 minutes

### MVP outputs
- OHLC
- Previous close
- % change
- gap
- day range
- ATR
- historical volatility
- moving averages
- RSI
- MACD
- ADX
- Bollinger Bands
- volume / turnover where available
- India VIX
- market breadth where available
- futures OI
- option chain
- PCR
- call/put OI concentration
- change in OI
- IV
- Greeks when available
- max-pain-like concentration indicator
- support/resistance clusters
- regime classification
- next-session scenario probabilities
- long/short/no-trade recommendation
- entry, target and stop zones
- time-window estimates
- risk/reward ratio
- expected range
- confidence score
- data quality score

## 6. Data-provider strategy

### Marketstack
Use as an optional EOD adapter.

Free Marketstack is useful for:
- end-of-day stock data
- limited historical EOD data
- symbol/exchange metadata

It is not sufficient as the sole provider for:
- Indian option chains
- derivatives OI
- option Greeks
- high-frequency/intraday analysis
- reliable next-day time-window modelling

### Recommended Indian-market primary adapter
**Upstox Developer API**, where access is available, for:
- NIFTY 50 market quotes
- historical candles
- intraday candles
- live WebSocket market data
- option contracts
- put/call option chain
- open interest
- option Greeks
- India VIX
- Indian IPO endpoints

### Official validation/reference source
**NSE India reports**
- F&O UDiFF bhavcopy
- daily settlement prices
- participant-wise OI
- participant-wise volumes
- FII derivatives statistics
- volatility reports
- contract specifications

### Forex expansion
Provider adapter compatible with **Twelve Data** or another FX provider.

## 7. Target personas

### Primary
Active Indian F&O trader who wants a disciplined daily plan.

### Secondary
- positional trader
- portfolio investor
- research analyst
- IPO investor

## 8. Core user stories

### Daily market brief
As a trader, I want to see today's NIFTY OHLC, trend, volatility, major levels and F&O positioning so that I understand the market state.

### Tomorrow strategy
As a trader, I want a quantified next-session plan with multiple scenarios so that I know what to do if NIFTY opens gap-up, flat or gap-down.

### Trade setup
As a trader, I want an entry zone, invalidation, stop and targets so that I can define risk before entering.

### Timing model
As a trader, I want an estimated probability window for entry and targets so that I know when historically similar setups tend to develop.

### F&O selection
As an options trader, I want the system to recommend an expiry/strike-selection framework based on liquidity, delta, IV and expected move.

### Multi-horizon outlook
As an investor, I want probability-based directional forecasts for 1 week, 1 month, 3 months, 6 months and 1 year.

### IPO screener
As an IPO investor, I want each IPO scored on valuation, growth, profitability, cash flow, debt, issue structure, subscription and risk.

## 9. Analysis framework

### Layer A — Raw market state
- OHLC
- returns
- gaps
- range
- volume
- OI
- IV
- VIX

### Layer B — Technical state
- trend
- momentum
- volatility
- mean-reversion
- support/resistance

### Layer C — Derivatives state
- futures basis
- OI build-up
- PCR
- option OI walls
- IV skew
- Greeks
- expiry effects

### Layer D — Regime model
Classify market into:
- strong bullish trend
- weak bullish trend
- range-bound
- weak bearish trend
- strong bearish trend
- high-volatility event regime

### Layer E — Forecast ensemble
Use several independent models:
- statistical expected-range model
- trend model
- mean-reversion model
- gradient-boosted classifier/regressor
- optional sequence model
- similarity / nearest-regime model

The final result is an ensemble, not a single-model prediction.

## 10. Strategy output format

```json
{
  "symbol": "NIFTY50",
  "session": "YYYY-MM-DD",
  "bias": "BULLISH",
  "confidence": 0.68,
  "expected_open": {
    "low": 0,
    "high": 0
  },
  "expected_day_range": {
    "low": 0,
    "high": 0
  },
  "primary_setup": {
    "direction": "LONG",
    "entry_zone": [0, 0],
    "confirmation": "15m close above X with breadth confirmation",
    "stop": 0,
    "targets": [0, 0, 0],
    "rr_to_t1": 0,
    "entry_time_window": ["09:45", "11:15"],
    "target_time_windows": [
      ["11:00", "13:00"],
      ["12:00", "14:45"]
    ],
    "invalidation": "..."
  },
  "alternative_setup": {},
  "no_trade_conditions": [],
  "risk": "HIGH"
}
```

## 11. Multi-horizon forecast
For every horizon:
- expected return range
- probability positive
- probability negative
- volatility estimate
- confidence/calibration
- major levels

Horizons:
- next session
- 1 week
- 1 month
- 3 months
- 6 months
- 1 year

## 12. IPO scoring
Score 0–100.

Suggested components:
- Revenue growth: 10
- EBITDA/PAT growth: 10
- ROE/ROCE: 10
- operating cash flow quality: 10
- debt: 10
- valuation vs peers: 15
- fresh issue vs OFS: 5
- promoter quality/governance: 10
- industry outlook: 5
- institutional demand/subscription: 10
- risk flags: ±5

Classification:
- 80–100: Strong candidate
- 65–79: Consider
- 50–64: Watch
- <50: Avoid / insufficient margin of safety

GMP must never be treated as authoritative.

## 13. Success metrics
- data ingestion success >99%
- no stale-data strategy generation
- every recommendation includes stop/invalidation
- Brier score / calibration tracked
- directional hit-rate tracked
- target hit-rate tracked
- max adverse excursion tracked
- max favorable excursion tracked
- simulated strategy expectancy tracked
- drawdown tracked
- false-confidence rate tracked

## 14. Non-goals for MVP
- automatic broker order execution
- guaranteed profit
- exact guaranteed price/time prediction
- high-frequency trading
- autonomous leverage decisions
- personalized financial advice without explicit risk settings

## 15. Release roadmap

### Phase 1
NIFTY 50 EOD research + next-day strategy.

### Phase 2
NIFTY live/intraday feed + F&O option chain.

### Phase 3
Backtesting + model calibration + paper trading.

### Phase 4
NSE F&O stocks.

### Phase 5
Forex/global indices.

### Phase 6
IPO research agent.

### Phase 7
Optional broker execution with hard risk controls.
