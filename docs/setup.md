# Setup Guide

## 1. Prerequisites

- AWS account with permissions for Lex, Lambda, DynamoDB, IAM, CodeBuild, CodeDeploy, and CodePipeline.
- AWS CLI configured (`aws configure`).
- Python 3.12+
- `zip` installed locally.

## 2. Clone and Install

```bash
git clone <your-fork-url>
cd AWS_Chatbot
pip install -r requirements.txt
```

## 3. Validate Locally

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## 4. Deploy Infrastructure

```bash
chmod +x scripts/deploy_pipeline.sh
./scripts/deploy_pipeline.sh banking-chatbot-stack <artifact-bucket-name> us-east-1
```

## 5. Create AWS Lex Bot

Use the AWS Lex V2 console and configure intents from `docs/tutorial/lex2.md`:

- `CheckBalanceIntent`
- `TransferFundsIntent`
- `RecentTransactionsIntent`
- Fallback intent

Set the fulfillment Lambda function to the deployed Lambda output from CloudFormation.

## 6. Connect CI/CD

- Enable GitHub Actions in your repository.
- Create AWS pipeline stages (source/build/deploy) as described in `docs/tutorial/lex5.md`.
- Ensure artifact bucket exists before pipeline creation.
