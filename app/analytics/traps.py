"""Public reference trap-risk engine.

This module intentionally contains transparent, configurable heuristic checks rather
than proprietary production weights. A private package can provide a calibrated
implementation using the same ``detect_traps`` contract.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class TrapPolicy:
    oversized_gap: float = 0.10
    gap_fade: float = 0.15
    opening_range_failure: float = 0.15
    vwap_failure: float = 0.10
    weak_breadth: float = 0.10
    futures_divergence: float = 0.10
    iv_shock: float = 0.08
    regime_conflict: float = 0.07
    low_volume: float = 0.07
    rejection_wick: float = 0.05
    options_non_confirmation: float = 0.08
    nearby_oi_wall: float = 0.05


def detect_traps(technical: dict, fno: dict, context: dict | None = None, policy: TrapPolicy | None = None) -> dict:
    """Return a transparent trap-risk score in the range 0..1.

    The defaults are examples for software demonstration and must be calibrated on
    walk-forward data before any real-money use.
    """
    context = context or {}
    policy = policy or TrapPolicy()
    flags: list[dict] = []

    def add(name: str, severity: float, reason: str) -> None:
        flags.append({"name": name, "severity": round(severity, 4), "reason": reason})

    gap_pct = float(context.get("gap_pct") or 0)
    first15_return = context.get("first15_return")
    vwap_distance = context.get("vwap_distance")
    breadth = context.get("breadth_pct")
    futures_basis_pct = context.get("futures_basis_pct")
    iv_jump_pct = context.get("iv_jump_pct")
    opening_range_failure = bool(context.get("opening_range_failure", False))

    atr_pct = float(technical.get("atr_pct") or 0.01)
    close_loc = float(technical.get("close_location") or 0.5)
    volz = float(technical.get("volume_z20") or 0)
    trend = float(technical.get("trend_score") or 0)

    if abs(gap_pct) > max(0.0075, atr_pct * 0.70):
        add("OVERSIZED_GAP", policy.oversized_gap, "Gap is large relative to recent ATR.")
    if gap_pct > 0 and first15_return is not None and first15_return < -abs(gap_pct) * 0.35:
        add("GAP_UP_FADE", policy.gap_fade, "Gap-up is fading during the opening phase.")
    if gap_pct < 0 and first15_return is not None and first15_return > abs(gap_pct) * 0.35:
        add("GAP_DOWN_REVERSAL", policy.gap_fade, "Gap-down is reversing during the opening phase.")
    if opening_range_failure:
        add("OPENING_RANGE_FAILURE", policy.opening_range_failure, "Breakout failed back inside the opening range.")
    if vwap_distance is not None and gap_pct > 0 and vwap_distance < -0.0015:
        add("VWAP_REJECTION", policy.vwap_failure, "Price lost VWAP after a bullish opening impulse.")
    if vwap_distance is not None and gap_pct < 0 and vwap_distance > 0.0015:
        add("VWAP_RECLAIM", policy.vwap_failure, "Price reclaimed VWAP after a bearish opening impulse.")
    if breadth is not None and gap_pct > 0 and breadth < 48:
        add("WEAK_BREADTH_BREAKOUT", policy.weak_breadth, "Index strength lacks broad participation.")
    if breadth is not None and gap_pct < 0 and breadth > 52:
        add("WEAK_BREADTH_BREAKDOWN", policy.weak_breadth, "Index weakness lacks broad participation.")
    if futures_basis_pct is not None and gap_pct > 0 and futures_basis_pct < -0.001:
        add("FUTURES_DIVERGENCE", policy.futures_divergence, "Futures basis does not confirm the bullish move.")
    if futures_basis_pct is not None and gap_pct < 0 and futures_basis_pct > 0.001:
        add("FUTURES_DIVERGENCE", policy.futures_divergence, "Futures basis does not confirm the bearish move.")
    if iv_jump_pct is not None and iv_jump_pct > 0.12:
        add("IV_SHOCK", policy.iv_shock, "Option IV expanded sharply; whipsaw risk is elevated.")
    if abs(trend) < 0.25 and abs(gap_pct) > 0.004:
        add("REGIME_CONFLICT", policy.regime_conflict, "Large move conflicts with weak higher-timeframe trend.")
    if volz < -0.5 and abs(gap_pct) > 0.004:
        add("LOW_VOLUME_MOVE", policy.low_volume, "Price expansion lacks volume confirmation.")
    if gap_pct > 0 and close_loc < 0.30:
        add("UPPER_REJECTION_WICK", policy.rejection_wick, "Price closed in the lower part of its range.")
    if gap_pct < 0 and close_loc > 0.70:
        add("LOWER_REJECTION_WICK", policy.rejection_wick, "Price closed in the upper part of its range.")

    pcr = fno.get("pcr_oi")
    call_wall = fno.get("call_wall")
    put_wall = fno.get("put_wall")
    spot = technical.get("close")
    if pcr is not None and gap_pct > 0 and pcr < 0.65:
        add("OPTIONS_NOT_CONFIRMING_UPMOVE", policy.options_non_confirmation, "PCR does not confirm the bullish move.")
    if pcr is not None and gap_pct < 0 and pcr > 1.35:
        add("OPTIONS_NOT_CONFIRMING_DOWNMOVE", policy.options_non_confirmation, "PCR does not confirm the bearish move.")
    if spot and call_wall and 0 < (call_wall - spot) / spot < 0.004:
        add("NEAR_CALL_WALL", policy.nearby_oi_wall, "Call OI concentration is immediately overhead.")
    if spot and put_wall and 0 < (spot - put_wall) / spot < 0.004:
        add("NEAR_PUT_WALL", policy.nearby_oi_wall, "Put OI concentration is immediately below.")

    score = min(1.0, sum(item["severity"] for item in flags))
    return {
        "trap_score": round(score, 4),
        "risk": "HIGH" if score >= 0.55 else "MEDIUM" if score >= 0.25 else "LOW",
        "flags": flags,
        "policy": asdict(policy),
        "calibration_warning": "Reference heuristics only; calibrate thresholds/weights with walk-forward data.",
    }
