# MarketPilot Core

**MarketPilot Core** is the open-source foundation for a modular market-research and F&O analytics platform. The reference implementation focuses on NSE NIFTY 50, while the interfaces are asset-agnostic so additional NSE instruments, forex, commodities and other markets can be added later.

> Research software only. Futures and options are leveraged products and can cause substantial losses. The reference strategy and trap weights are examples, not validated trading advice. `NO_TRADE` is a first-class outcome.

## Public-core / private-alpha design

This repository is intentionally suitable for public GitHub hosting. Keep proprietary alpha in a separate private repository/package such as `marketpilot-alpha`.

**Public `marketpilot-core`:** provider adapters, schemas, indicators, generic F&O analytics, generic trap-risk checks, API/UI scaffolding, backtesting interfaces, documentation and tests.

**Private `marketpilot-alpha`:** trained model artifacts, calibrated feature weights, proprietary entry/exit ranking, execution logic, position-sizing IP, production prompts, broker/account data and live trading records.

The extension protocols are in `app/analytics/extensions.py`.

## Features

- Marketstack EOD adapter
- Upstox Indian-market adapter
- NIFTY historical-data research pipeline
- option-chain/F&O analytics
- technical indicators and regime classifier
- configurable fake-jump/fake-breakout reference engine
- baseline probabilistic forecast engine
- strategy/risk gate with `TRADE` / `NO_TRADE`
- IPO research service scaffolding
- FastAPI API
- minimal browser dashboard
- Docker configuration
- pytest tests
- GitHub Actions CI
- Apache-2.0 license
- security and contribution policies

## Reference fake-move factors

The public engine can flag oversized gaps, gap fades/reversals, opening-range failure, VWAP failure, weak breadth, futures-basis divergence, IV shock, regime conflict, weak volume, rejection wicks, option-PCR non-confirmation and nearby OI walls. These are intentionally transparent heuristics. Production implementations should calibrate them by regime using walk-forward tests and may replace the module through the extension interface.

## Quick start

```bash
git clone https://github.com/YOUR-ORG/marketpilot-core.git
cd marketpilot-core
python -m venv .venv
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Then:

```bash
pip install -e ".[dev]"
cp .env.example .env      # Windows: copy .env.example .env
pytest -q
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Configuration

Never commit credentials. Put API keys and tokens in `.env` locally and use repository/environment secrets in CI or deployment systems.

Typical variables:

```env
MARKETSTACK_API_KEY=
UPSTOX_CLIENT_ID=
UPSTOX_CLIENT_SECRET=
UPSTOX_ACCESS_TOKEN=
DATABASE_URL=
```

## Repository layout

```text
marketpilot-core/
├── app/
│   ├── analytics/
│   ├── api/
│   ├── core/
│   ├── providers/
│   ├── schemas/
│   ├── services/
│   └── templates/
├── docs/
├── scripts/
├── tests/
├── .github/workflows/ci.yml
├── CONTRIBUTING.md
├── LICENSE
├── NOTICE
├── SECURITY.md
├── OPEN_SOURCE_STRATEGY.md
└── README.md
```

## How a private alpha package plugs in

A private package should implement the protocols from `app.analytics.extensions` and be loaded through configuration/dependency injection. Do not hardcode private imports into the public repository.

Example conceptual layout:

```text
marketpilot-alpha/
├── marketpilot_alpha/
│   ├── calibrated_traps.py
│   ├── forecast_models.py
│   ├── strategy_models.py
│   └── risk_models.py
└── model_artifacts/
```

## Testing

```bash
pytest -q
ruff check .
```

Before a release, also run data-provider contract tests with test/sandbox credentials and a full walk-forward backtest outside CI.

## Open-source publication checklist

1. Search the entire Git history for API keys, tokens, customer/account data and proprietary model artifacts.
2. Rotate any credential that has ever been committed.
3. Keep `.env`, model files, live trade data and proprietary configuration out of the public repo.
4. Publish under Apache-2.0 only if you accept its permissive reuse terms and patent grant.
5. Add `SECURITY.md`, `CONTRIBUTING.md`, issue/PR templates and Code of Conduct if community participation is desired.
6. Protect `main` with a GitHub ruleset requiring pull requests and passing CI.
7. Enable secret scanning/push protection where available.
8. Create a signed/tagged `v0.1.0` release.
9. Never represent the reference heuristics as profitable or production-validated unless evidence supports that claim.

See `OPEN_SOURCE_LAUNCH_GUIDE.md` for the detailed publication process.

## License

Apache License 2.0. See `LICENSE` and `NOTICE`.
