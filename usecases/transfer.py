from usecases.repositories.transactioncontextinterface import (
    TransactionContextInterface as tContext
)
from usecases.repositories.accountsrepositoryinterface import (
    AccountsRepositoryInterface as accRepo,
    BankAccount
)
from usecases.contexterrors.accountdoesnotexistserror import (
    AccountDoesNotExistsError
)
from domain.bankaccount import Amount
from domain.commontypes.types import AccountId


class TransferFundsUseCase:
    def __init__(self,
                 acc_repository: accRepo,
                 transactional_context: tContext
                 ):
        self.acc_repository = acc_repository
        self.transactional_context = transactional_context

    def execute(self,
                acc_id: AccountId,
                dest_id: AccountId,
                amount: Amount
                ) -> bool:
        with self.transactional_context:
            get_existence = self.acc_repository.exists
            both_exists = get_existence(acc_id) and get_existence(dest_id)
            if not both_exists:
                raise AccountDoesNotExistsError(dest_id)

            maybe_account = self.acc_repository.get_by_id(acc_id)

            def transfer_to(account: BankAccount):
                account.transfer(dest_id, amount)
                self.acc_repository.update(account)

            maybe_account.run(transfer_to)

        if self.transactional_context.get_errors():
            return False
        else:
            return True
