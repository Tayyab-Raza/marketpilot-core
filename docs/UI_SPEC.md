# UI_SPEC — MarketPilot AI

## 1. Design goal
A trader should understand the system's view in under 60 seconds.

Desktop-first responsive dashboard.

## 2. Main navigation
- Dashboard
- NIFTY 50
- F&O
- Forecasts
- Strategy
- Backtests
- IPOs
- Performance
- Data Status
- Settings

## 3. Daily dashboard

### Header
```text
NIFTY 50 | Session: 05 Oct 2026 | Data Complete ✓
Bias: BULLISH 68% | Regime: Trend | Risk: Medium
```

### Card row 1 — Today
- Open
- High
- Low
- Close
- Change %
- Day range %
- ATR
- India VIX

### Card row 2 — Technical state
- RSI
- ADX
- MACD
- 20 DMA
- 50 DMA
- 200 DMA
- trend score

### Main price chart
Candlestick:
- support zones
- resistance zones
- moving averages
- predicted next-session range
- proposed entry
- stop
- T1/T2/T3

## 4. F&O panel

Show:
- nearest expiry
- futures basis
- futures OI and change
- PCR OI
- PCR volume
- ATM IV
- implied move
- call wall
- put wall

Option-chain table:
```text
CALL OI | CALL ΔOI | CALL IV | CALL LTP | STRIKE | PUT LTP | PUT IV | PUT ΔOI | PUT OI
```

Highlight:
- top call OI
- top put OI
- top change in OI
- ATM

## 5. Tomorrow strategy page

### Section A — Executive view
```text
PRIMARY BIAS
Bullish: 62%
Bearish: 25%
Range:   13%

Expected Range:
24,420 – 24,810
```

### Section B — Primary setup
```text
Direction: LONG
Entry zone: 24,480–24,520
Confirmation: 15m close above 24,520
Stop: 24,390
T1: 24,620
T2: 24,720
T3: 24,800
```

### Section C — Time probabilities
Do NOT show false exactness.

```text
Entry-zone first-touch probability
09:15–09:45  ███ 18%
09:45–10:30  ███████ 36%
10:30–11:30  █████ 25%
After 11:30   ████ 21%
```

Target timing:
same pattern.

### Section D — Alternate scenario
Show bearish setup separately.

### Section E — No-trade conditions
Large visible warning box.

Examples:
- gap exceeds model expected range
- India VIX shock
- first 15m closes below invalidation
- bid/ask spreads abnormal
- conflicting OI structure

## 6. Multi-horizon page

Table:
| Horizon | Bullish % | Expected Return Range | Expected Volatility | Confidence |
|---|---:|---:|---:|---:|
| 1 day | | | | |
| 1 week | | | | |
| 1 month | | | | |
| 3 months | | | | |
| 6 months | | | | |
| 1 year | | | | |

Chart:
probability fan / quantile band.

## 7. Backtest page
Show:
- total setups
- win rate
- expectancy
- profit factor
- max drawdown
- calibration
- equity curve (paper simulation)
- monthly results
- setup performance by regime

Mandatory warning if sample size is small.

## 8. Performance page
Forecast honesty dashboard:

```text
Predicted 60–70% confidence bucket
Actual success rate: 64%
Calibration: GOOD
```

This is critical to prevent the AI from appearing more certain than it is.

## 9. IPO page

### IPO table
- Company
- Open/close
- Price band
- Issue size
- Mainboard/SME
- Subscription
- Score
- Recommendation

### IPO detail
Sections:
- business
- use of proceeds
- financial growth
- margins
- cash flow
- debt
- valuation
- peer comparison
- promoter/governance
- issue mix
- subscription
- risks
- final score

Recommendation badges:
- Strong Candidate
- Consider
- Watch
- Avoid
- Insufficient Data

## 10. Data-status page
For each provider:
- connected/disconnected
- latest timestamp
- latency
- quota/rate-limit
- capabilities

## 11. Mobile
Mobile home shows only:
1. bias
2. expected range
3. setup
4. stop
5. targets
6. no-trade conditions

## 12. UX safeguards
- always show "data as of"
- always show model confidence
- always show invalidation
- never use "guaranteed"
- never display exact future timestamp without probability context
- differentiate actual prices vs model levels
