from datetime import datetime, date, timedelta, timezone
import httpx
from app.core.config import settings
from app.schemas.market import Candle, MarketSnapshot, OptionRow, OptionLeg

class UpstoxProvider:
    name = "upstox"

    def __init__(self):
        self.base = settings.upstox_base_url.rstrip("/")
        self.token = settings.upstox_access_token

    def _headers(self):
        if not self.token:
            raise RuntimeError("UPSTOX_ACCESS_TOKEN is not configured")
        return {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}

    async def get_historical_candles(self, instrument: str, days: int = 260) -> list[Candle]:
        to_d = date.today()
        from_d = to_d - timedelta(days=max(days * 2, 370))
        key = instrument.replace("|", "%7C").replace(" ", "%20")
        url = f"{self.base}/v3/historical-candle/{key}/days/1/{to_d}/{from_d}"
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(url, headers=self._headers())
            r.raise_for_status()
            rows = r.json().get("data", {}).get("candles", [])
        out = []
        for row in reversed(rows[-days:]):
            ts, o, h, l, c, v, *rest = row
            oi = rest[0] if rest else 0
            out.append(Candle(ts=datetime.fromisoformat(ts), open=o, high=h, low=l, close=c,
                              volume=v or 0, oi=oi or 0))
        return out

    async def get_snapshot(self, instrument: str) -> MarketSnapshot:
        params = {"instrument_key": instrument}
        url = f"{self.base}/v3/market-quote/ohlc"
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(url, params=params, headers=self._headers())
            if r.status_code == 404:
                url = f"{self.base}/v2/market-quote/ohlc"
                r = await client.get(url, params={"instrument_key": instrument, "interval": "1d"}, headers=self._headers())
            r.raise_for_status()
            payload = r.json().get("data", {})
        row = next(iter(payload.values())) if payload else {}
        live = row.get("live_ohlc") or row.get("ohlc") or {}
        prev = row.get("prev_ohlc") or {}
        spot = row.get("last_price") or live.get("close")
        return MarketSnapshot(
            symbol=instrument,
            as_of=datetime.now(timezone.utc),
            spot=float(spot),
            previous_close=float(row.get("prev_close_price") or prev.get("close") or 0) or None,
            open=float(live.get("open") or 0) or None,
            high=float(live.get("high") or 0) or None,
            low=float(live.get("low") or 0) or None,
            volume=float(live.get("volume") or row.get("volume") or 0) or None,
        )

    async def get_option_chain(self, instrument: str, expiry: str | None = None) -> dict:
        if expiry is None:
            contracts_url = f"{self.base}/v2/option/contract"
            async with httpx.AsyncClient(timeout=30) as client:
                rr = await client.get(contracts_url, params={"instrument_key": instrument}, headers=self._headers())
                rr.raise_for_status()
                contracts = rr.json().get("data", [])
            expiries = sorted({x.get("expiry") for x in contracts if x.get("expiry")})
            if not expiries:
                return {"expiry": None, "rows": []}
            expiry = expiries[0]
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(f"{self.base}/v2/option/chain", params={"instrument_key": instrument, "expiry_date": expiry}, headers=self._headers())
            r.raise_for_status()
            data = r.json().get("data", [])
        rows: list[OptionRow] = []
        for x in data:
            def leg(side: str) -> OptionLeg:
                md = (x.get(side) or {}).get("market_data", {})
                gr = (x.get(side) or {}).get("option_greeks", {})
                return OptionLeg(
                    ltp=md.get("ltp"), oi=md.get("oi"), oi_change=md.get("oi_change"),
                    volume=md.get("volume"), iv=gr.get("iv"), delta=gr.get("delta"),
                    gamma=gr.get("gamma"), theta=gr.get("theta"), vega=gr.get("vega")
                )
            rows.append(OptionRow(strike=float(x.get("strike_price")), call=leg("call_options"), put=leg("put_options")))
        return {"expiry": expiry, "rows": rows}

    async def get_ipos(self, status: str = "open") -> list[dict]:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(f"{self.base}/v2/ipos", params={"status": status, "records": 30}, headers=self._headers())
            r.raise_for_status()
            return r.json().get("data", [])
