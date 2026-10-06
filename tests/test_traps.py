from app.analytics.traps import detect_traps

def test_fake_gap_scores_high_when_multiple_failures():
    tech={"atr_pct":.01,"close_location":.2,"volume_z20":-1,"trend_score":0,"close":25000}
    fno={"pcr_oi":.5,"call_wall":25050,"put_wall":24800}
    ctx={"gap_pct":.012,"first15_return":-.008,"vwap_distance":-.003,"breadth_pct":40,"opening_range_failure":True}
    r=detect_traps(tech,fno,ctx)
    assert r["trap_score"] >= .6
    assert r["risk"] == "HIGH"
