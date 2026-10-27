# Tutorial Stage 3: Lambda Fulfillment + DynamoDB

This stage implements backend logic.

## Components

- `src/banking_chatbot/fulfillment.py`
  - Intent routing
  - Slot validation
  - Response generation for Lex V2
- DynamoDB tables
  - Accounts table (primary key: `accountId`)
  - Transactions table (primary key: `accountId`)

## Key Behaviors

- Reject malformed and non-positive transfer amounts.
- Return clear user messages for missing accounts and empty transaction history.
- Keep intent handlers isolated for maintainability and testability.

## Validation

Run:

```bash
python -m unittest discover -s tests -p "test_*.py"
```
