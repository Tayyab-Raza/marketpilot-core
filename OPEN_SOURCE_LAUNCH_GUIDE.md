# MarketPilot Core — Open-Source Launch Guide

This repository is designed to be the public half of an open-core architecture.

## 1. Keep these public
- provider interfaces and adapters
- normalized market schemas
- generic indicators and F&O analytics
- transparent reference trap heuristics
- API/UI framework
- generic backtesting/evaluation tools
- documentation and tests

## 2. Keep these private
- broker/client credentials and refresh tokens
- customer/account identifiers
- live orders/trades and account balances
- proprietary datasets you are not licensed to redistribute
- trained model artifacts and calibrated production weights
- private alpha features and strategy-ranking logic
- production position sizing and execution rules
- production LLM prompts if they contain proprietary logic

## 3. Pre-publication security audit
1. Copy only public-safe files into the public repository.
2. Delete caches, local databases, notebooks with embedded outputs, `.env` files and model artifacts.
3. Search for secrets using your preferred scanner plus manual searches for `token`, `secret`, `password`, `api_key`, `access_token`, account IDs and email addresses.
4. Inspect Git history. Deleting a secret from the latest file does not remove it from history.
5. Rotate every credential that was ever committed or shared accidentally.
6. Verify third-party market data can legally be redistributed before checking any sample dataset into Git.

## 4. Create the GitHub repository
Recommended name: `marketpilot-core`.

Create an organization first if you want the project to have a brand independent of a personal GitHub account. Create the repository as private initially, push the cleaned code, perform the security review, then switch it to public.

## 5. Initialize and push
```bash
git init
git branch -M main
git add .
git commit -m "Initial public release of MarketPilot Core"
git remote add origin git@github.com:YOUR-ORG/marketpilot-core.git
git push -u origin main
```

## 6. Repository settings
Recommended `main` ruleset:
- require a pull request before merge
- require at least one approval once external contributors are active
- dismiss stale approvals after new commits
- require status checks / CI
- block force pushes
- block branch deletion
- optionally require signed commits

Enable secret scanning/push protection where available. Add Dependabot/security update tooling if appropriate for your organization.

## 7. License
This package includes Apache License 2.0.

Apache-2.0 permits broad use, modification and distribution, including commercial use, subject to its terms. It also contains an explicit patent-license provision. Do not use the license casually if you want to prevent competitors from commercially reusing the public core; in that case, obtain legal advice about an alternative model before publication.

## 8. Community files
Keep:
- `README.md`
- `LICENSE`
- `NOTICE`
- `CONTRIBUTING.md`
- `SECURITY.md`

Recommended additions as the community grows:
- `CODE_OF_CONDUCT.md`
- issue templates
- pull-request template
- `CHANGELOG.md`
- maintainer/governance policy

## 9. First release
Use semantic versioning.

Suggested first tag:
```bash
git tag -a v0.1.0 -m "MarketPilot Core v0.1.0"
git push origin v0.1.0
```

Create a GitHub Release from the tag. State clearly that it is an experimental research framework and not a validated trading product.

## 10. Private alpha repository
Create `marketpilot-alpha` as PRIVATE.

Store production implementations there and depend on the public core:
```text
marketpilot-alpha/
├── marketpilot_alpha/
│   ├── calibrated_traps.py
│   ├── proprietary_features.py
│   ├── forecast_models.py
│   ├── strategy_models.py
│   ├── execution.py
│   └── position_sizing.py
├── model_artifacts/
└── tests/
```

Use private package/repository access in deployment. Do not copy the private code into GitHub Actions logs or public issue discussions.

## 11. Contribution model
Use branches such as `feat/...`, `fix/...`, and `docs/...`.

External flow:
1. fork
2. feature branch
3. tests
4. pull request
5. CI
6. maintainer review
7. squash/merge

Do not accept contributions that embed scraped/licensed market datasets without confirming redistribution rights.

## 12. Disclosure policy
Security issues should follow `SECURITY.md`, not public issues. Clearly define which versions you support.

## 13. Trading-specific publication rules
- do not claim guaranteed returns
- do not publish cherry-picked backtests as proof
- disclose transaction-cost/slippage assumptions
- distinguish research signals from broker execution
- keep exact account/risk settings private
- ensure data licensing permits redistribution
- preserve immutable forecasts when publishing performance statistics

## 14. Release checklist
- tests pass
- lint passes
- no secrets
- no proprietary artifacts
- no prohibited data redistribution
- README updated
- changelog/release notes ready
- version bumped
- release tag signed if possible
- CI green

## 15. Recommended long-term model
Public core builds adoption and integrations. Private alpha retains the commercial edge. If you later commercialize hosted analytics, users can run the public infrastructure while paying for proprietary models, premium datasets or managed service features.
