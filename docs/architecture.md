# Architecture

## Core Runtime Architecture

The chatbot runtime consists of:

1. **AWS Lex V2 Bot** for intent classification and slot collection.
2. **AWS Lambda fulfillment function** (`src/banking_chatbot/fulfillment.py`) for business logic.
3. **DynamoDB accounts table** for account balances.
4. **DynamoDB transactions table** for recent transaction lookups.

### Runtime Interaction

```mermaid
sequenceDiagram
    participant User
    participant Lex as AWS Lex V2
    participant Lambda as Fulfillment Lambda
    participant DDB as DynamoDB

    User->>Lex: "What's my account balance?"
    Lex->>Lambda: Intent + slot payload
    Lambda->>DDB: Read account by accountId
    DDB-->>Lambda: Account record
    Lambda-->>Lex: Fulfillment message
    Lex-->>User: Natural language response
```

## CI/CD Architecture

```mermaid
flowchart LR
    GH[GitHub Push / PR] --> GHA[GitHub Actions]
    GHA --> CP[CodePipeline Source/Build/Deploy]
    CP --> CB[CodeBuild]
    CB --> CD[CodeDeploy Lambda Deployment]
    CD --> LAMBDA[Updated Fulfillment Function]
```

## Security and Reliability Baselines

- IAM role uses least privilege access to DynamoDB and CloudWatch logs.
- Runtime configuration is provided through environment variables.
- Unit tests gate packaging in both GitHub Actions and CodeBuild.
- Deployment workflow supports repeatable releases through infrastructure templates.
