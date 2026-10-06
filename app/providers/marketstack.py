from datetime import datetime, timezone
import httpx
from app.core.config import settings
from app.providers.base import CapabilityNotSupported
from app.schemas.market import Candle, MarketSnapshot

class MarketstackProvider:
    name = "marketstack"

    def __init__(self):
        self.key = settings.marketstack_api_key
        self.base = settings.marketstack_base_url.rstrip("/")

    def _auth(self):
        if not self.key:
            raise RuntimeError("MARKETSTACK_API_KEY is not configured")
        return {"access_key": self.key}

    async def get_historical_candles(self, instrument: str, days: int = 260) -> list[Candle]:
        params = self._auth() | {"symbols": instrument, "limit": min(days, 1000)}
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(f"{self.base}/eod", params=params)
            r.raise_for_status()
            rows = r.json().get("data", [])
        out = []
        for x in reversed(rows):
            out.append(Candle(
                ts=datetime.fromisoformat(x["date"].replace("Z", "+00:00")),
                open=float(x["open"]), high=float(x["high"]), low=float(x["low"]),
                close=float(x["close"]), volume=float(x.get("volume") or 0), oi=0,
            ))
        return out

    async def get_snapshot(self, instrument: str) -> MarketSnapshot:
        candles = await self.get_historical_candles(instrument, 2)
        if not candles:
            raise RuntimeError("No Marketstack EOD data")
        c = candles[-1]
        prev = candles[-2].close if len(candles) > 1 else None
        return MarketSnapshot(symbol=instrument, as_of=c.ts, spot=c.close, previous_close=prev,
                              open=c.open, high=c.high, low=c.low, volume=c.volume)

    async def get_option_chain(self, instrument: str, expiry: str | None = None) -> dict:
        raise CapabilityNotSupported("Marketstack is not the F&O option-chain provider in this project")

    async def get_ipos(self, status: str = "open") -> list[dict]:
        raise CapabilityNotSupported("Use Upstox/official sources for IPO discovery")
