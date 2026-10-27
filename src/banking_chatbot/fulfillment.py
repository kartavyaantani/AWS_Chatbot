"""AWS Lex V2 fulfillment logic for a sample banking chatbot."""

from __future__ import annotations

import os
from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Account:
    account_id: str
    owner_name: str
    available_balance: Decimal


@dataclass(frozen=True)
class Transaction:
    account_id: str
    description: str
    amount: Decimal


class AccountRepository:
    """Repository for account data access."""

    def get_account(self, account_id: str) -> Optional[Account]:
        raise NotImplementedError

    def apply_transfer(self, source_id: str, destination_id: str, amount: Decimal) -> bool:
        raise NotImplementedError


class TransactionRepository:
    """Repository for transaction data access."""

    def list_recent(self, account_id: str, limit: int = 5) -> List[Transaction]:
        raise NotImplementedError


class DynamoAccountRepository(AccountRepository):
    def __init__(self, table_name: str):
        import boto3

        self._table = boto3.resource("dynamodb").Table(table_name)

    def get_account(self, account_id: str) -> Optional[Account]:
        response = self._table.get_item(Key={"accountId": account_id})
        item = response.get("Item")
        if not item:
            return None

        return Account(
            account_id=item["accountId"],
            owner_name=item.get("ownerName", "Customer"),
            available_balance=Decimal(str(item.get("availableBalance", "0"))),
        )

    def apply_transfer(self, source_id: str, destination_id: str, amount: Decimal) -> bool:
        source = self.get_account(source_id)
        destination = self.get_account(destination_id)

        if not source or not destination:
            return False
        if source.available_balance < amount:
            return False

        self._table.update_item(
            Key={"accountId": source_id},
            UpdateExpression="SET availableBalance = availableBalance - :amount",
            ExpressionAttributeValues={":amount": amount},
        )

        self._table.update_item(
            Key={"accountId": destination_id},
            UpdateExpression="SET availableBalance = availableBalance + :amount",
            ExpressionAttributeValues={":amount": amount},
        )

        return True


class DynamoTransactionRepository(TransactionRepository):
    def __init__(self, table_name: str):
        import boto3

        self._table = boto3.resource("dynamodb").Table(table_name)

    def list_recent(self, account_id: str, limit: int = 5) -> List[Transaction]:
        response = self._table.query(
            KeyConditionExpression="accountId = :account",
            ExpressionAttributeValues={":account": account_id},
            Limit=limit,
            ScanIndexForward=False,
        )
        items = response.get("Items", [])
        return [
            Transaction(
                account_id=i["accountId"],
                description=i.get("description", "Transaction"),
                amount=Decimal(str(i.get("amount", "0"))),
            )
            for i in items
        ]


class BankingFulfillmentService:
    def __init__(
        self,
        accounts: AccountRepository,
        transactions: TransactionRepository,
    ):
        self.accounts = accounts
        self.transactions = transactions

    def handle_intent(self, intent_name: str, slots: Dict[str, Dict[str, str]]) -> str:
        handlers = {
            "CheckBalanceIntent": self._check_balance,
            "TransferFundsIntent": self._transfer_funds,
            "RecentTransactionsIntent": self._recent_transactions,
            "FallbackIntent": lambda _s: "I can help with balance checks, transfers, or recent transactions.",
        }

        handler = handlers.get(intent_name)
        if not handler:
            return "Sorry, I did not understand that request."
        return handler(slots)

    def _check_balance(self, slots: Dict[str, Dict[str, str]]) -> str:
        account_id = _slot_value(slots, "AccountId")
        if not account_id:
            return "Please share the account ID to check your balance."

        account = self.accounts.get_account(account_id)
        if not account:
            return f"I couldn't find account {account_id}."

        return (
            f"{account.owner_name}, the available balance for account {account.account_id} "
            f"is ${account.available_balance:,.2f}."
        )

    def _transfer_funds(self, slots: Dict[str, Dict[str, str]]) -> str:
        source_id = _slot_value(slots, "SourceAccountId")
        destination_id = _slot_value(slots, "DestinationAccountId")
        amount_raw = _slot_value(slots, "Amount")

        if not source_id or not destination_id or not amount_raw:
            return "Please provide source account, destination account, and amount."

        try:
            amount = Decimal(amount_raw)
        except Exception:
            return "Please provide a valid numeric transfer amount."

        if amount <= 0:
            return "Transfer amount must be greater than zero."

        success = self.accounts.apply_transfer(source_id, destination_id, amount)
        if not success:
            return "Transfer failed. Check account details and available balance."

        return (
            f"Transfer of ${amount:,.2f} from {source_id} to {destination_id} was successful."
        )

    def _recent_transactions(self, slots: Dict[str, Dict[str, str]]) -> str:
        account_id = _slot_value(slots, "AccountId")
        if not account_id:
            return "Please share the account ID to list recent transactions."

        records = self.transactions.list_recent(account_id)
        if not records:
            return f"No recent transactions were found for account {account_id}."

        summary = "; ".join(
            f"{t.description}: ${t.amount:,.2f}" for t in records
        )
        return f"Recent transactions for {account_id}: {summary}."


def _slot_value(slots: Dict[str, Dict[str, str]], slot_name: str) -> Optional[str]:
    slot = slots.get(slot_name) or {}
    value = slot.get("value") or {}
    interpreted = value.get("interpretedValue")
    return interpreted.strip() if interpreted else None


def _lex_close_message(message: str) -> Dict[str, object]:
    return {
        "sessionState": {"dialogAction": {"type": "Close"}, "intent": {"state": "Fulfilled"}},
        "messages": [{"contentType": "PlainText", "content": message}],
    }


def _build_service() -> BankingFulfillmentService:
    account_table = os.getenv("ACCOUNT_TABLE", "banking-accounts")
    transaction_table = os.getenv("TRANSACTION_TABLE", "banking-transactions")
    return BankingFulfillmentService(
        accounts=DynamoAccountRepository(account_table),
        transactions=DynamoTransactionRepository(transaction_table),
    )


def lambda_handler(event: Dict[str, object], _context: object) -> Dict[str, object]:
    interpretation = (event.get("interpretations") or [{}])[0]
    intent = interpretation.get("intent") or {}
    intent_name = intent.get("name", "FallbackIntent")
    slots = intent.get("slots") or {}

    service = _build_service()
    reply = service.handle_intent(intent_name, slots)

    response = _lex_close_message(reply)
    response["sessionState"]["intent"] = {
        "name": intent_name,
        "state": "Fulfilled",
    }
    return response
