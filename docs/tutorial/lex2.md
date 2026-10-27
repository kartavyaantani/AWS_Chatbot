# Tutorial Stage 2: Build the AWS Lex Bot

This stage focuses on Lex conversational design.

## Intents

1. **CheckBalanceIntent**
   - Slots: `AccountId`
2. **TransferFundsIntent**
   - Slots: `SourceAccountId`, `DestinationAccountId`, `Amount`
3. **RecentTransactionsIntent**
   - Slots: `AccountId`
4. **FallbackIntent**

## Suggested Utterances

- "Check balance for account {AccountId}"
- "Transfer {Amount} from {SourceAccountId} to {DestinationAccountId}"
- "Show recent transactions for {AccountId}"

## Fulfillment Configuration

- Enable Lambda code hook for all core intents.
- Set fulfillment to deployed handler `fulfillment.lambda_handler`.
