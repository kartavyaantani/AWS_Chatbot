import unittest
from decimal import Decimal

from src.banking_chatbot.fulfillment import (
    Account,
    BankingFulfillmentService,
    Transaction,
)


class FakeAccountRepository:
    def __init__(self):
        self.accounts = {
            "ACC100": Account("ACC100", "Jordan", Decimal("2500.50")),
            "ACC200": Account("ACC200", "Casey", Decimal("450.25")),
        }

    def get_account(self, account_id):
        return self.accounts.get(account_id)

    def apply_transfer(self, source_id, destination_id, amount):
        source = self.accounts.get(source_id)
        destination = self.accounts.get(destination_id)
        if not source or not destination or source.available_balance < amount:
            return False

        self.accounts[source_id] = Account(
            source.account_id,
            source.owner_name,
            source.available_balance - amount,
        )
        self.accounts[destination_id] = Account(
            destination.account_id,
            destination.owner_name,
            destination.available_balance + amount,
        )
        return True


class FakeTransactionRepository:
    def list_recent(self, account_id, limit=5):
        if account_id == "ACC100":
            return [
                Transaction(account_id, "Coffee Shop", Decimal("8.75")),
                Transaction(account_id, "Salary", Decimal("1200.00")),
            ]
        return []


def lex_slots(**kwargs):
    return {k: {"value": {"interpretedValue": v}} for k, v in kwargs.items()}


class FulfillmentTests(unittest.TestCase):
    def setUp(self):
        self.service = BankingFulfillmentService(FakeAccountRepository(), FakeTransactionRepository())

    def test_balance_lookup_success(self):
        message = self.service.handle_intent("CheckBalanceIntent", lex_slots(AccountId="ACC100"))
        self.assertIn("$2,500.50", message)

    def test_transfer_validation_for_negative_amount(self):
        message = self.service.handle_intent(
            "TransferFundsIntent",
            lex_slots(SourceAccountId="ACC100", DestinationAccountId="ACC200", Amount="-15"),
        )
        self.assertEqual("Transfer amount must be greater than zero.", message)

    def test_transfer_success(self):
        message = self.service.handle_intent(
            "TransferFundsIntent",
            lex_slots(SourceAccountId="ACC100", DestinationAccountId="ACC200", Amount="50"),
        )
        self.assertIn("was successful", message)

    def test_recent_transactions(self):
        message = self.service.handle_intent("RecentTransactionsIntent", lex_slots(AccountId="ACC100"))
        self.assertIn("Coffee Shop", message)

    def test_fallback_message(self):
        message = self.service.handle_intent("UnknownIntent", {})
        self.assertIn("did not understand", message)


if __name__ == "__main__":
    unittest.main()
