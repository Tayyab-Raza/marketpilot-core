# DATA_MODEL — MarketPilot AI

## 1. Database
PostgreSQL.

Use UUID primary keys for business entities and composite uniqueness for market bars.

## 2. Core tables

### instruments
```sql
id UUID PRIMARY KEY
canonical_symbol TEXT UNIQUE NOT NULL
name TEXT NOT NULL
asset_class TEXT NOT NULL
exchange TEXT
currency TEXT
timezone TEXT NOT NULL
active BOOLEAN DEFAULT TRUE
metadata JSONB
created_at TIMESTAMPTZ
updated_at TIMESTAMPTZ
```

### provider_instruments
```sql
id UUID PRIMARY KEY
instrument_id UUID REFERENCES instruments(id)
provider TEXT NOT NULL
provider_symbol TEXT NOT NULL
provider_instrument_key TEXT
metadata JSONB
UNIQUE(provider, provider_symbol)
```

### candles
```sql
instrument_id UUID REFERENCES instruments(id)
interval TEXT NOT NULL
ts TIMESTAMPTZ NOT NULL
open NUMERIC(20,8)
high NUMERIC(20,8)
low NUMERIC(20,8)
close NUMERIC(20,8)
volume NUMERIC(30,8)
open_interest NUMERIC(30,8)
provider TEXT NOT NULL
is_final BOOLEAN DEFAULT FALSE
ingested_at TIMESTAMPTZ
PRIMARY KEY(instrument_id, interval, ts, provider)
```

### market_quotes
```sql
id BIGSERIAL PRIMARY KEY
instrument_id UUID
ts TIMESTAMPTZ
ltp NUMERIC
open NUMERIC
high NUMERIC
low NUMERIC
prev_close NUMERIC
volume NUMERIC
oi NUMERIC
bid NUMERIC
ask NUMERIC
provider TEXT
payload JSONB
```

## 3. Derivatives

### derivative_contracts
```sql
id UUID PRIMARY KEY
underlying_instrument_id UUID
instrument_type TEXT
expiry DATE
strike NUMERIC
option_type TEXT
lot_size INT
provider_instrument_key TEXT
exchange TEXT
active BOOLEAN
metadata JSONB
```

### option_chain_snapshots
```sql
id UUID PRIMARY KEY
underlying_instrument_id UUID
expiry DATE
snapshot_ts TIMESTAMPTZ
spot_price NUMERIC
provider TEXT
data_quality_score NUMERIC
```

### option_chain_rows
```sql
snapshot_id UUID REFERENCES option_chain_snapshots(id)
strike NUMERIC
call_ltp NUMERIC
call_oi NUMERIC
call_oi_change NUMERIC
call_volume NUMERIC
call_iv NUMERIC
call_delta NUMERIC
call_gamma NUMERIC
call_theta NUMERIC
call_vega NUMERIC
put_ltp NUMERIC
put_oi NUMERIC
put_oi_change NUMERIC
put_volume NUMERIC
put_iv NUMERIC
put_delta NUMERIC
put_gamma NUMERIC
put_theta NUMERIC
put_vega NUMERIC
PRIMARY KEY(snapshot_id, strike)
```

### futures_snapshots
```sql
id UUID PRIMARY KEY
underlying_instrument_id UUID
contract_id UUID
snapshot_ts TIMESTAMPTZ
ltp NUMERIC
basis NUMERIC
volume NUMERIC
oi NUMERIC
oi_change NUMERIC
provider TEXT
```

## 4. Features

### feature_sets
```sql
id UUID PRIMARY KEY
instrument_id UUID
as_of_ts TIMESTAMPTZ
timeframe TEXT
feature_version TEXT
features JSONB
source_hash TEXT
created_at TIMESTAMPTZ
UNIQUE(instrument_id, as_of_ts, timeframe, feature_version)
```

## 5. Models

### model_registry
```sql
id UUID PRIMARY KEY
name TEXT
task TEXT
version TEXT
trained_from DATE
trained_to DATE
feature_version TEXT
metrics JSONB
artifact_uri TEXT
active BOOLEAN
created_at TIMESTAMPTZ
```

### forecasts
```sql
id UUID PRIMARY KEY
instrument_id UUID
as_of_ts TIMESTAMPTZ
target_session DATE
horizon TEXT
model_version TEXT
p_up NUMERIC
p_down NUMERIC
p_range NUMERIC
expected_return NUMERIC
q10 NUMERIC
q25 NUMERIC
q50 NUMERIC
q75 NUMERIC
q90 NUMERIC
confidence NUMERIC
calibration_score NUMERIC
explanation JSONB
created_at TIMESTAMPTZ
```

## 6. Strategies

### strategy_reports
```sql
id UUID PRIMARY KEY
instrument_id UUID
as_of_ts TIMESTAMPTZ
target_session DATE
bias TEXT
confidence NUMERIC
risk_level TEXT
expected_low NUMERIC
expected_high NUMERIC
regime TEXT
model_versions JSONB
data_snapshot_hash TEXT
frozen BOOLEAN DEFAULT TRUE
created_at TIMESTAMPTZ
```

### trade_setups
```sql
id UUID PRIMARY KEY
report_id UUID REFERENCES strategy_reports(id)
name TEXT
direction TEXT
instrument_preference TEXT
entry_low NUMERIC
entry_high NUMERIC
confirmation TEXT
stop NUMERIC
target1 NUMERIC
target2 NUMERIC
target3 NUMERIC
invalidation TEXT
entry_window_start TIME
entry_window_end TIME
entry_touch_probability NUMERIC
target_windows JSONB
risk_reward JSONB
no_trade_conditions JSONB
```

## 7. Forecast evaluation

### forecast_outcomes
```sql
forecast_id UUID PRIMARY KEY REFERENCES forecasts(id)
actual_open NUMERIC
actual_high NUMERIC
actual_low NUMERIC
actual_close NUMERIC
actual_return NUMERIC
direction_correct BOOLEAN
evaluated_at TIMESTAMPTZ
```

### setup_outcomes
```sql
setup_id UUID PRIMARY KEY REFERENCES trade_setups(id)
entry_touched BOOLEAN
entry_first_touch_ts TIMESTAMPTZ
stop_touched BOOLEAN
t1_touched BOOLEAN
t2_touched BOOLEAN
t3_touched BOOLEAN
max_adverse_excursion NUMERIC
max_favorable_excursion NUMERIC
result_r NUMERIC
evaluated_at TIMESTAMPTZ
```

## 8. IPO

### ipos
```sql
id UUID PRIMARY KEY
provider TEXT
provider_ipo_id TEXT
company_name TEXT
issue_type TEXT
status TEXT
open_date DATE
close_date DATE
listing_date DATE
price_low NUMERIC
price_high NUMERIC
lot_size INT
issue_size NUMERIC
fresh_issue NUMERIC
ofs_size NUMERIC
metadata JSONB
UNIQUE(provider, provider_ipo_id)
```

### ipo_fundamentals
```sql
ipo_id UUID REFERENCES ipos(id)
period_end DATE
revenue NUMERIC
ebitda NUMERIC
pat NUMERIC
net_worth NUMERIC
debt NUMERIC
operating_cash_flow NUMERIC
roe NUMERIC
roce NUMERIC
eps NUMERIC
PRIMARY KEY(ipo_id, period_end)
```

### ipo_scores
```sql
id UUID PRIMARY KEY
ipo_id UUID
as_of_ts TIMESTAMPTZ
score NUMERIC
recommendation TEXT
confidence NUMERIC
components JSONB
risks JSONB
explanation TEXT
```

## 9. Agent runs

### agent_runs
```sql
id UUID PRIMARY KEY
agent_name TEXT
started_at TIMESTAMPTZ
completed_at TIMESTAMPTZ
status TEXT
input_ref JSONB
output_ref JSONB
error JSONB
trace_id TEXT
```

## 10. Data lineage
Each analytical record must be reproducible from:
- exact input snapshot
- feature version
- model version
- strategy version
- source provider
- timestamps
