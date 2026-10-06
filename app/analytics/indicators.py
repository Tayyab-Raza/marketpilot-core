from __future__ import annotations
import numpy as np
import pandas as pd
from app.schemas.market import Candle

def candles_to_df(candles: list[Candle]) -> pd.DataFrame:
    if not candles:
        return pd.DataFrame()
    df = pd.DataFrame([c.model_dump() for c in candles]).set_index("ts").sort_index()
    return df

def ema(s: pd.Series, n: int):
    return s.ewm(span=n, adjust=False).mean()

def rsi(close: pd.Series, n: int = 14):
    d = close.diff()
    up = d.clip(lower=0).ewm(alpha=1/n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False).mean()
    rs = up / dn.replace(0, np.nan)
    return 100 - 100/(1+rs)

def atr(df: pd.DataFrame, n: int = 14):
    pc = df.close.shift(1)
    tr = pd.concat([(df.high-df.low), (df.high-pc).abs(), (df.low-pc).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1/n, adjust=False).mean()

def adx(df: pd.DataFrame, n: int = 14):
    up = df.high.diff()
    down = -df.low.diff()
    plus_dm = up.where((up > down) & (up > 0), 0.0)
    minus_dm = down.where((down > up) & (down > 0), 0.0)
    a = atr(df, n)
    plus_di = 100 * plus_dm.ewm(alpha=1/n, adjust=False).mean() / a.replace(0, np.nan)
    minus_di = 100 * minus_dm.ewm(alpha=1/n, adjust=False).mean() / a.replace(0, np.nan)
    dx = 100 * (plus_di-minus_di).abs()/(plus_di+minus_di).replace(0, np.nan)
    return dx.ewm(alpha=1/n, adjust=False).mean()

def technical_summary(candles: list[Candle]) -> dict:
    df = candles_to_df(candles)
    if len(df) < 30:
        return {"status":"INSUFFICIENT_HISTORY"}
    close = df.close
    a = atr(df)
    macd_line = ema(close,12)-ema(close,26)
    signal = ema(macd_line,9)
    ret = close.pct_change()
    rv20 = ret.rolling(20).std()*np.sqrt(252)
    out = {
        "close": float(close.iloc[-1]),
        "ret_1d": float(ret.iloc[-1] or 0),
        "ret_5d": float(close.iloc[-1]/close.iloc[-6]-1) if len(close)>6 else None,
        "sma20": float(close.rolling(20).mean().iloc[-1]),
        "sma50": float(close.rolling(50).mean().iloc[-1]) if len(close)>=50 else None,
        "sma200": float(close.rolling(200).mean().iloc[-1]) if len(close)>=200 else None,
        "ema20": float(ema(close,20).iloc[-1]),
        "rsi14": float(rsi(close).iloc[-1]),
        "atr14": float(a.iloc[-1]),
        "atr_pct": float(a.iloc[-1]/close.iloc[-1]),
        "adx14": float(adx(df).iloc[-1]),
        "macd": float(macd_line.iloc[-1]),
        "macd_signal": float(signal.iloc[-1]),
        "realized_vol20": float(rv20.iloc[-1]) if not np.isnan(rv20.iloc[-1]) else None,
        "rolling_high20": float(df.high.rolling(20).max().iloc[-1]),
        "rolling_low20": float(df.low.rolling(20).min().iloc[-1]),
        "range_pct": float((df.high.iloc[-1]-df.low.iloc[-1])/close.iloc[-1]),
        "close_location": float((close.iloc[-1]-df.low.iloc[-1]) / max(df.high.iloc[-1]-df.low.iloc[-1],1e-9)),
        "volume_z20": float((df.volume.iloc[-1]-df.volume.rolling(20).mean().iloc[-1]) / max(df.volume.rolling(20).std().iloc[-1],1e-9)) if df.volume.sum()>0 else 0.0,
    }
    bull = 0
    bull += 1 if out["close"] > out["sma20"] else -1
    if out["sma50"] is not None: bull += 1 if out["close"] > out["sma50"] else -1
    bull += 1 if out["macd"] > out["macd_signal"] else -1
    bull += 1 if out["rsi14"] >= 50 else -1
    out["trend_score"] = bull/4
    return out
