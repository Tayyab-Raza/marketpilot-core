from __future__ import annotations
import numpy as np
from app.schemas.market import Candle
from app.analytics.indicators import candles_to_df

def baseline_forecast(candles: list[Candle], technical: dict, regime: dict, fno: dict) -> dict:
    df = candles_to_df(candles)
    rets = df.close.pct_change().dropna()
    if len(rets) < 60:
        return {"status":"INSUFFICIENT_HISTORY"}
    recent = rets.tail(min(252,len(rets)))
    mu = float(recent.mean())
    sigma = float(recent.std())
    trend = float(technical.get("trend_score") or 0)
    momentum = float(technical.get("ret_5d") or 0)
    pcr = fno.get("pcr_oi")
    options_tilt = 0 if pcr is None else max(-.08,min(.08,(pcr-1)*.12))
    logit = trend*.7 + np.tanh(momentum*18)*.25 + options_tilt
    p_up = 1/(1+np.exp(-logit))
    uncertainty = min(.22, max(.10, sigma*4))
    p_range = uncertainty
    p_up = float(p_up*(1-p_range))
    p_down = float(1-p_range-p_up)
    close = float(df.close.iloc[-1])
    atr = float(technical.get("atr14") or close*sigma)
    q = {
        "q10": close - 1.25*atr,
        "q25": close - .65*atr,
        "q50": close*(1+mu+trend*.0008),
        "q75": close + .65*atr,
        "q90": close + 1.25*atr,
    }
    return {"status":"OK","p_up":round(p_up,4),"p_down":round(p_down,4),"p_range":round(p_range,4),
            "expected_return":mu+trend*.0008,"expected_low":q["q10"],"expected_high":q["q90"],"quantiles":q,
            "model":"baseline-ensemble-v1"}

def horizon_forecast(candles: list[Candle], technical: dict) -> list[dict]:
    df = candles_to_df(candles)
    rets = df.close.pct_change().dropna()
    mu = float(rets.tail(252).mean()) if len(rets) else 0
    sd = float(rets.tail(252).std()) if len(rets) else .01
    trend = float(technical.get("trend_score") or 0)
    horizons = [("1w",5),("1m",21),("3m",63),("6m",126),("1y",252)]
    out=[]
    for name,n in horizons:
        expected = mu*n + trend*.002*np.sqrt(n)
        vol = sd*np.sqrt(n)
        z = expected/max(vol,1e-9)
        p = float(1/(1+np.exp(-1.7*z)))
        out.append({"horizon":name,"probability_positive":round(p,3),"expected_return":round(expected,4),
                    "return_low":round(expected-1.28*vol,4),"return_high":round(expected+1.28*vol,4),
                    "volatility":round(vol,4)})
    return out
