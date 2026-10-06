from app.providers.factory import get_provider
from app.analytics.indicators import technical_summary
from app.analytics.fno import fno_summary
from app.analytics.regime import classify_regime
from app.analytics.forecast import baseline_forecast, horizon_forecast
from app.analytics.traps import detect_traps
from app.analytics.strategy import generate_strategy

NIFTY = "NSE_INDEX|Nifty 50"

async def run_research(provider_name: str | None = None, context: dict | None = None) -> dict:
    p = get_provider(provider_name)
    candles = await p.get_historical_candles(NIFTY, 320)
    snapshot = await p.get_snapshot(NIFTY)
    try:
        oc = await p.get_option_chain(NIFTY)
        rows = oc.get("rows", [])
        expiry = oc.get("expiry")
    except Exception as e:
        rows=[]; expiry=None
    tech = technical_summary(candles)
    fno = fno_summary(rows, snapshot.spot)
    reg = classify_regime(tech, snapshot.india_vix)
    fc = baseline_forecast(candles, tech, reg, fno)
    traps = detect_traps(tech, fno, context)
    strat = generate_strategy(tech, fno, reg, fc, traps)
    return {
        "instrument":"NIFTY 50","provider":p.name,"data_as_of":snapshot.as_of.isoformat(),
        "today":{"spot":snapshot.spot,"open":snapshot.open,"high":snapshot.high,"low":snapshot.low,
                 "previous_close":snapshot.previous_close,"volume":snapshot.volume},
        "technical":tech,"fno":fno,"option_expiry":expiry,"regime":reg,"forecast":fc,
        "horizons":horizon_forecast(candles,tech),"trap_analysis":traps,"strategy":strat,
        "disclaimer":"Probabilistic research output, not a guaranteed forecast or investment advice."
    }
