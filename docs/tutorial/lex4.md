# Tutorial Stage 4: Build and Packaging Automation

This stage creates repeatable build artifacts.

## Files

- `buildspec.yml` for CodeBuild
- `scripts/package_lambda.sh` for Lambda artifact generation
- `appspec.yml` for CodeDeploy Lambda deployments

## Pipeline Build Steps

1. Install Python dependencies.
2. Execute unit tests.
3. Package Lambda source and dependencies as `dist/lambda.zip`.
4. Publish artifact for deployment stages.

## Validation

```bash
chmod +x scripts/package_lambda.sh
./scripts/package_lambda.sh
```
