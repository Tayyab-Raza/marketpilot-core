from app.analytics.strategy import generate_strategy

def base():
    t={"close":25000,"atr14":200,"rolling_low20":24500,"rolling_high20":25500}
    f={"put_wall":24700,"call_wall":25400}
    r={"regime":"BULLISH_TREND"}
    fc={"status":"OK","p_up":.72,"p_down":.18,"p_range":.10,"expected_low":24750,"expected_high":25400}
    return t,f,r,fc

def test_strategy_can_trade():
    t,f,r,fc=base(); tr={"trap_score":.05,"flags":[]}
    s=generate_strategy(t,f,r,fc,tr)
    assert s["action"] in {"TRADE","NO_TRADE"}

def test_strategy_blocks_high_trap():
    t,f,r,fc=base(); tr={"trap_score":.8,"flags":[]}
    s=generate_strategy(t,f,r,fc,tr)
    assert s["action"] == "NO_TRADE"
