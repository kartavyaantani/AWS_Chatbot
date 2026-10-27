# Tutorial Stage 5: CI/CD Integration

This stage connects source control to deployment automation.

## GitHub Actions

Workflow file: `.github/workflows/ci-cd.yml`

- Runs tests for pushes and pull requests.
- Builds Lambda package artifact after tests succeed.

## AWS Pipeline

Use CloudFormation and AWS Developer Tools for deployment:

- **CodePipeline**: source, build, deploy orchestration
- **CodeBuild**: executes `buildspec.yml`
- **CodeDeploy**: updates Lambda alias/version using `appspec.yml`

## Suggested Production Enhancements

- Add branch protections and required checks.
- Introduce integration tests with Lex test events.
- Add canary traffic shifting and rollback alarms.
