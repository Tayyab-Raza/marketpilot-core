# Security policy

## Secrets
Never commit API tokens or broker credentials.

Use environment variables or a managed secret store.

## If a secret is exposed
1. Revoke/rotate it immediately.
2. Remove it from repository history.
3. Review access logs.
4. Reissue least-privilege credentials.

## Trading-specific security
Before live execution, implement:
- authentication/authorization on admin routes
- encrypted token storage
- audit log
- IP/network restrictions where supported
- order idempotency
- kill switch
- daily loss limits
- read-only mode by default

## Responsible disclosure
For a public project, create a private vulnerability-reporting channel before accepting security reports.
