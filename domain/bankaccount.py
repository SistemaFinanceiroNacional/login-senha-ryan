from typing import List

from domain.ledgeraccount import LedgerAccount
from domain.transaction import Transaction, create_transaction
from domain.commontypes.types import AccountID, Amount


class BankAccount:
    def __init__(self,
                 account_id: AccountID,
                 main_account: LedgerAccount,
                 draft_account: LedgerAccount,
                 stage_account: LedgerAccount,
                 overdraft_limit: Amount
                 ):
        self._id = account_id
        self._main_account = main_account
        self._draft_account = draft_account
        self._stage_account = stage_account
        self._overdraft_limit = overdraft_limit

    def get_balance(self) -> Amount:
        main_balance = self._main_account.get_balance()
        draft_balance = self._draft_account.get_balance()
        return main_balance - draft_balance

    def transfer(self, destiny_id: AccountID, value: Amount) -> None:
        if value <= 0:
            raise InvalidValueToTransfer(value)

        main_balance = self._main_account.get_balance()
        main_id = self._main_account.account_id

        main_transaction = create_transaction(main_id, destiny_id, value)
        if main_balance >= value:
            self._main_account.add_transaction(main_transaction)
            return

        remaining = value - main_balance
        draft_account_balance = self._draft_account.get_balance()
        overdraft = self._overdraft_limit - draft_account_balance

        if overdraft < remaining:
            raise InsufficientFundsException(self.get_balance(), value)

        draft_id = self._draft_account.account_id
        draft_transaction = create_transaction(draft_id, main_id, remaining)

        self._draft_account.add_transaction(draft_transaction)
        self._main_account.add_transaction(draft_transaction)
        self._main_account.add_transaction(main_transaction)

    def get_id(self) -> AccountID:
        return self._id

    def get_transactions(self) -> List[Transaction]:
        main_transactions = self._main_account.get_transactions()
        stage_transactions = self._stage_account.get_transactions()
        draft_transactions = self._draft_account.get_transactions()
        all_transactions = []
        all_transactions.extend(main_transactions)
        all_transactions.extend(draft_transactions)
        all_transactions.extend(stage_transactions)
        return all_transactions


class InsufficientFundsException(Exception):
    def __init__(self, balance: Amount, value: Amount):
        super().__init__(f"{balance} is insufficient to get {value}")


class InvalidValueToTransfer(Exception):
    def __init__(self, value: Amount):
        super().__init__(f"{value} is a non-positive value to transfer.")
