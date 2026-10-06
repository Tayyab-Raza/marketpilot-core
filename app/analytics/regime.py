def classify_regime(t: dict, vix: float | None = None) -> dict:
    if t.get("status") == "INSUFFICIENT_HISTORY": return {"regime":"UNKNOWN","confidence":0}
    score = float(t.get("trend_score") or 0)
    adx = float(t.get("adx14") or 0)
    high_vol = (vix or 0) >= 20 or (t.get("realized_vol20") or 0) >= .24
    if score >= .5 and adx >= 20: regime = "VOLATILE_BULL" if high_vol else "BULLISH_TREND"
    elif score <= -.5 and adx >= 20: regime = "VOLATILE_BEAR" if high_vol else "BEARISH_TREND"
    else: regime = "HIGH_VOL_RANGE" if high_vol else "RANGE"
    conf = min(.9, .5 + abs(score)*.25 + min(adx,40)/200)
    return {"regime":regime,"confidence":round(conf,3)}
