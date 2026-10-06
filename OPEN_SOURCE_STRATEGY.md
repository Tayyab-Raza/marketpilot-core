# Open-source strategy

## Recommendation
Use an **open-core** structure rather than publishing the entire trading system.

## Why
Publishing infrastructure can attract developers, testing and provider integrations. Publishing calibrated alpha logic can remove your information advantage and make cloning trivial.

## Public repository
Recommended name: `marketpilot-core`

Publish:
- interfaces
- provider adapters that do not contain keys
- normalized schemas
- generic indicators
- generic trap-detection framework with example/default weights
- generic backtesting library
- UI shell
- API server
- docs
- tests
- example configuration

License recommendation: Apache License 2.0.

Apache-2.0 is permissive and also includes an explicit patent license, making it suitable for a developer-facing infrastructure project.

## Private repository
Recommended name: `marketpilot-alpha`

Keep private:
- final factor weights
- proprietary features
- private datasets
- model checkpoints
- exact trained parameters
- feature-selection results
- production strategy rules
- live fills and P&L
- broker integrations if they expose sensitive operational controls
- credentials/secrets

## Public/private package boundary
A clean design is:

```text
marketpilot-core/
  marketpilot/
    providers/
    schemas/
    indicators/
    backtest/
    api/

marketpilot-alpha/   # private
  alpha/
    features/
    models/
    strategy/
    execution/
```

The private package imports the public one.

## GitHub publication checklist
1. Create a new organization or repository.
2. Add `LICENSE` (Apache-2.0 for the public core).
3. Add `README.md`.
4. Add `CONTRIBUTING.md`.
5. Add `SECURITY.md`.
6. Add `.gitignore` and secret scanning.
7. Add GitHub Actions for tests/linting.
8. Enable Dependabot.
9. Require pull-request review on `main`.
10. Enable branch protection.
11. Never push a real `.env`.
12. Rotate any key accidentally committed; deleting the commit is not enough.
13. Use GitHub Releases and semantic versioning.
14. Clearly state that trading examples are research, not guarantees.

## When not to open source
Keep the whole project private if:
- your primary goal is proprietary trading performance rather than developer adoption;
- the system's main value is its exact feature/weight/model combination;
- you have not yet separated secrets and proprietary modules cleanly;
- you intend to commercialize access before building a contributor ecosystem.

## Recommended decision for this project
Open-source the **core infrastructure later**, after the private/public boundary is clean. Keep the live alpha engine private from day one.
