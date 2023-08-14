from typing import List

from domain.ledgeraccount import LedgerAccount
from domain.bankaccounttransaction import (
    BankAccountTransaction,
    create_transaction
)
from domain.commontypes.types import AccountId, Amount


class BankAccount:
    def __init__(self,
                 account_id: AccountId,
                 main_account: LedgerAccount,
                 draft_account: LedgerAccount,
                 stage_account: LedgerAccount,
                 overdraft_limit: Amount
                 ):
        self._id = account_id
        self._main_account = main_account
        self._draft_account = draft_account
        self.stage_account = stage_account
        self._overdraft_limit = overdraft_limit

    def get_balance(self) -> Amount:
        main_balance = self._main_account.get_balance()
        draft_balance = self._draft_account.get_balance()
        return main_balance - draft_balance

    def transfer(self, destiny_id: AccountId, value: Amount) -> None:
        if value <= 0:
            raise InvalidValueToTransfer(value)

        main_balance = self._main_account.get_balance()
        main_id = self._main_account.account_id

        if main_balance < value:
            self.use_overdraft(value, main_balance, main_id)

        main_transaction = create_transaction(main_id, destiny_id, value)
        self._main_account.add_transaction(main_transaction)

    def use_overdraft(
            self,
            value: Amount,
            main_balance: Amount,
            main_id: AccountId
    ):
        remaining = value - main_balance
        draft_account_balance = self._draft_account.get_balance()
        overdraft = self._overdraft_limit - draft_account_balance

        if overdraft < remaining:
            raise InsufficientFundsException(self.get_balance(), value)

        draft_id = self._draft_account.account_id
        draft_transaction = create_transaction(draft_id, main_id, remaining)

        self._draft_account.add_transaction(draft_transaction)
        self._main_account.add_transaction(draft_transaction)

    def get_id(self) -> AccountId:
        return self._id

    def get_transactions(self) -> List[BankAccountTransaction]:
        main_transactions = self._main_account.get_transactions()
        stage_transactions = self.stage_account.get_transactions()
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
