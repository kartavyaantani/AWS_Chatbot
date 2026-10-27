# Operations Runbook

## Logging and Monitoring

- Lambda writes execution logs to CloudWatch Logs.
- Add CloudWatch alarms for:
  - Lambda error count
  - Lambda duration p95
  - Throttles for Lambda and DynamoDB

## Safe Release Process

1. Create feature branch.
2. Push changes and open pull request.
3. Ensure `ci-cd` workflow passes.
4. Merge to protected branch.
5. Verify CodePipeline deployment status.
6. Execute Lex regression checks.

## Manual Verification Checklist

- Balance intent returns expected amount for known account.
- Transfer intent rejects invalid and negative amounts.
- Transfer intent succeeds with sufficient balance.
- Recent transactions intent returns latest transactions.
- Unknown requests trigger fallback behavior.

## Incident Response

- Roll back Lambda alias in CodeDeploy if deployment fails health checks.
- Re-run pipeline from failed stage after remediation.
- For data incidents, restore affected records from DynamoDB backups.
