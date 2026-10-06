from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.research import run_research
from app.services.ipo import list_scored_ipos

app=FastAPI(title="MarketPilot AI",version="0.1.0",description="Probabilistic NIFTY F&O research engine")
templates=Jinja2Templates(directory="app/templates")

@app.get("/api/v1/health")
async def health(): return {"status":"ok"}

@app.get("/api/v1/research/nifty")
async def nifty(provider: str|None=None): return await run_research(provider)

@app.get("/api/v1/research/nifty/intraday-context")
async def nifty_context(
    gap_pct: float=0,
    first15_return: float|None=None,
    vwap_distance: float|None=None,
    breadth_pct: float|None=None,
    futures_basis_pct: float|None=None,
    iv_jump_pct: float|None=None,
    opening_range_failure: bool=False,
    provider: str|None=None,
):
    ctx=locals().copy(); ctx.pop("provider")
    return await run_research(provider,ctx)

@app.get("/api/v1/ipos")
async def ipos(status: str=Query("open",pattern="^(open|upcoming|closed|listed)$")):
    return await list_scored_ipos(status)

@app.get("/",response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})
