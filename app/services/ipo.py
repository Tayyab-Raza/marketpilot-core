from app.providers.factory import get_provider

def score_ipo(item: dict) -> dict:
    # Metadata-only preliminary score. Fundamental scoring requires prospectus/financial ingestion.
    score = 50
    reasons=[]; risks=[]
    sub = item.get("subscription") or item.get("total_subscription")
    if isinstance(sub,(int,float)):
        if sub >= 10: score += 10; reasons.append("Strong subscription")
        elif sub < 1: score -= 8; risks.append("Weak subscription")
    issue_type=(item.get("issue_type") or "").lower()
    if issue_type == "sme": risks.append("SME IPO: liquidity and volatility risk can be materially higher")
    rec = "CONSIDER" if score>=65 else "WATCH" if score>=50 else "AVOID"
    return {"score":score,"recommendation":rec,"reasons":reasons,"risks":risks,
            "note":"Preliminary score only; add prospectus financials, peer valuation, cash flow, debt and governance before investment decision."}

async def list_scored_ipos(status: str="open"):
    p=get_provider("upstox")
    items=await p.get_ipos(status)
    return [{"ipo":x,"analysis":score_ipo(x)} for x in items]
