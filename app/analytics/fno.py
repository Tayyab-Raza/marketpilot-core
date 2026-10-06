from __future__ import annotations
from app.schemas.market import OptionRow

def _nz(v): return float(v or 0)

def fno_summary(rows: list[OptionRow], spot: float) -> dict:
    if not rows:
        return {"status":"UNAVAILABLE"}
    call_oi = sum(_nz(x.call.oi) for x in rows)
    put_oi = sum(_nz(x.put.oi) for x in rows)
    call_vol = sum(_nz(x.call.volume) for x in rows)
    put_vol = sum(_nz(x.put.volume) for x in rows)
    call_wall = max(rows, key=lambda x:_nz(x.call.oi)).strike
    put_wall = max(rows, key=lambda x:_nz(x.put.oi)).strike
    call_doi_wall = max(rows, key=lambda x:_nz(x.call.oi_change)).strike
    put_doi_wall = max(rows, key=lambda x:_nz(x.put.oi_change)).strike
    atm = min(rows, key=lambda x:abs(x.strike-spot))
    atm_straddle = _nz(atm.call.ltp)+_nz(atm.put.ltp)
    ivs = [v for v in [_nz(atm.call.iv), _nz(atm.put.iv)] if v>0]
    atm_iv = sum(ivs)/len(ivs) if ivs else None
    return {
        "status":"OK",
        "pcr_oi": put_oi/call_oi if call_oi else None,
        "pcr_volume": put_vol/call_vol if call_vol else None,
        "call_wall":call_wall,
        "put_wall":put_wall,
        "call_doi_wall":call_doi_wall,
        "put_doi_wall":put_doi_wall,
        "atm_strike":atm.strike,
        "atm_iv":atm_iv,
        "atm_straddle":atm_straddle,
        "implied_move_pct":atm_straddle/spot if spot else None,
    }
