from datetime import datetime, date
from pydantic import BaseModel, Field

class Candle(BaseModel):
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float = 0
    oi: float = 0

class OptionLeg(BaseModel):
    ltp: float | None = None
    oi: float | None = None
    oi_change: float | None = None
    volume: float | None = None
    iv: float | None = None
    delta: float | None = None
    gamma: float | None = None
    theta: float | None = None
    vega: float | None = None

class OptionRow(BaseModel):
    strike: float
    call: OptionLeg = Field(default_factory=OptionLeg)
    put: OptionLeg = Field(default_factory=OptionLeg)

class MarketSnapshot(BaseModel):
    symbol: str = "NSE_INDEX|Nifty 50"
    as_of: datetime
    spot: float
    previous_close: float | None = None
    open: float | None = None
    high: float | None = None
    low: float | None = None
    volume: float | None = None
    india_vix: float | None = None
    futures_price: float | None = None
    futures_oi: float | None = None
    futures_oi_change: float | None = None
    option_expiry: date | None = None
    option_chain: list[OptionRow] = Field(default_factory=list)
