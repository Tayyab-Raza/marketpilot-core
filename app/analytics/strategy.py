from __future__ import annotations
from app.core.config import settings

def generate_strategy(technical: dict, fno: dict, regime: dict, forecast: dict, traps: dict) -> dict:
    if forecast.get("status") != "OK":
        return {"action":"NO_TRADE","reason":"Insufficient forecast history"}
    trap = float(traps.get("trap_score") or 0)
    confidence = max(forecast["p_up"], forecast["p_down"])
    confidence *= max(.35, 1-trap*.75)
    close = float(technical["close"]); atr = float(technical["atr14"])
    support = max(float(technical.get("rolling_low20") or close-atr), fno.get("put_wall") or -1e18)
    resistance = min(float(technical.get("rolling_high20") or close+atr), fno.get("call_wall") or 1e18)
    if trap >= settings.max_trap_score:
        return {"action":"NO_TRADE","confidence":round(confidence,3),"reason":"Fake-move/trap risk exceeds threshold","traps":traps}
    direction = "LONG" if forecast["p_up"] > forecast["p_down"] else "SHORT"
    if confidence < settings.min_strategy_confidence:
        return {"action":"NO_TRADE","confidence":round(confidence,3),"reason":"Confidence below threshold","traps":traps}
    if direction == "LONG":
        entry_low = max(close-.18*atr, support)
        entry_high = close+.08*atr
        stop = min(entry_low-.55*atr, support-.20*atr)
        t1 = max(entry_high+.65*atr, close+.55*atr)
        t2 = max(t1+.45*atr, resistance)
        t3 = t2+.60*atr
        confirmation = "5m/15m reclaim above entry-high with VWAP hold; breadth and futures must confirm."
        invalidation = "15m close below structural stop or trap score rises above threshold."
        option_pref = "ATM/slightly ITM CE; prefer liquid strike with controlled IV and bid-ask spread."
    else:
        entry_low = close-.08*atr
        entry_high = min(close+.18*atr, resistance)
        stop = max(entry_high+.55*atr, resistance+.20*atr)
        t1 = min(entry_low-.65*atr, close-.55*atr)
        t2 = min(t1-.45*atr, support)
        t3 = t2-.60*atr
        confirmation = "5m/15m rejection below entry-low with VWAP below price structure; breadth and futures must confirm."
        invalidation = "15m close above structural stop or trap score rises above threshold."
        option_pref = "ATM/slightly ITM PE; prefer liquid strike with controlled IV and bid-ask spread."
    risk = abs(((entry_low+entry_high)/2)-stop); reward=abs(t1-((entry_low+entry_high)/2))
    rr = reward/max(risk,1e-9)
    if rr < 1.05:
        return {"action":"NO_TRADE","confidence":round(confidence,3),"reason":"Insufficient risk/reward after structural levels","traps":traps}
    return {
        "action":"TRADE","direction":direction,"confidence":round(confidence,3),"regime":regime["regime"],
        "entry_zone":[round(entry_low,2),round(entry_high,2)],"stop":round(stop,2),
        "targets":[round(t1,2),round(t2,2),round(t3,2)],"rr_to_t1":round(rr,2),
        "confirmation":confirmation,"invalidation":invalidation,"option_preference":option_pref,
        "expected_range":[round(forecast["expected_low"],2),round(forecast["expected_high"],2)],
        "timing_note":"Exact future times are not claimed. Use intraday first-touch model once sufficient 1m/5m history is stored.",
        "traps":traps,
    }
