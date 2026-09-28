import logging
from typing import List

from usecases.get_transactions import TransactionData
from domain.amount import Amount
from domain.bankaccount import InsufficientFundsException
from domain.money import InvalidMoney, Money
from inputio.input_io import InputIO
from usecases.unlogged_cases import UnloggedUseCases
from usecases.logged_cases import LoggedUseCases
from usecases.contexterrors.accountdoesnotexistserror import (
    AccountDoesNotExistsError
)
from domain.commontypes.types import AccountID, ClientID
from infrastructure.authserviceinterface import AuthServiceInterface

logger = logging.getLogger("drivers.Cli.command_line_interface")


def transfer_money(io: InputIO, acc_id: AccountID, l_cases: LoggedUseCases):
    destination_account = int(io.input(
        "Enter the ID of the destination account: "
    ))
    try:
        amount = Amount(io.input("How much do you want to transfer? "))
        l_cases.transfer.execute(acc_id, destination_account, amount)
        io.print("Successful transaction.")
    except InsufficientFundsException:
        io.print("Insufficient funds.")
    except InvalidMoney as e:
        io.print(str(e))
    except AccountDoesNotExistsError:
        io.print("Invalid Account ID.")


def show_transactions(io: InputIO,
                      c_id: ClientID,
                      acc_id: AccountID,
                      l_cases: LoggedUseCases
                      ):
    maybe_transactions = l_cases.get_transactions.execute(c_id, acc_id)

    def transactions_print(transactions: List[TransactionData]) -> str:
        aux = ""
        for t in transactions:
            aux += str(t) + "\n"
        return aux

    default_message = "No transactions to show."
    msg = maybe_transactions.map(transactions_print).or_else(default_message)
    io.print(msg)


def accounts_repl(io: InputIO,
                  c_id: ClientID,
                  acc_id: AccountID,
                  l_cases: LoggedUseCases
                  ):
    balance_case = l_cases.get_balance

    def balance_print():
        maybe_balance = balance_case.execute(c_id, acc_id)
        default_message = "Error on trying to show your balance"

        def balance_message(balance: Money) -> str:
            return f"R${balance}"

        io.print(maybe_balance.map(balance_message).or_else(default_message))

    options = {
        "1": balance_print,
        "2": lambda: transfer_money(io, acc_id, l_cases),
        "3": lambda: show_transactions(io, c_id, acc_id, l_cases),
        "4": lambda: None
    }
    io.print("""
            (1) Balance
            (2) Transfer money
            (3) Extract
            (4) Exit account
        """)
    while True:
        command = io.input("->")
        if command in options:
            action = options[command]
            if command == "4":
                break
            action()


def repl(io: InputIO, c_id: ClientID, logged_cases: LoggedUseCases):
    io.print("""
            (1) Select account
            (2) Logout
    """)
    while True:
        command = io.input("->")
        if command == "1":
            accs = list(logged_cases.get_accounts.execute(c_id))
            for acc in accs:
                print(f"Account ID: {acc}")
            select_acc = int(io.input("Choose one ID: "))
            if select_acc in accs:
                accounts_repl(io, c_id, select_acc, logged_cases)
                io.print("""
            (1) Select account
            (2) Logout
                    """)
        elif command == "2":
            break


def main(io: InputIO,
         auth_service: AuthServiceInterface,
         unlogged_cases: UnloggedUseCases,
         logged_cases: LoggedUseCases
         ):
    while True:
        choice = io.input("Would you like to Sign In (1),"
                          " Create a new client account (2)"
                          " or Exit(3)? ")
        if choice == "1":
            username = io.input("Enter your username: ")
            password = io.inputoccult("Enter your password: ")
            if not username or not password:
                io.print("Login and password should not be empty.")
            else:
                logger.debug("Going to verify the account...")
                maybe_client_id = auth_service.authenticate(username, password)
                maybe_client_id.map(lambda client_id: repl(
                    io, client_id, logged_cases
                )).or_else(lambda: io.print("You are not logged in!"))

        elif choice == "2":
            username = io.input("Enter your new username: ")
            password = io.inputoccult("Enter your new password: ")
            if not username or not password:
                io.print("Login and password should not be empty.")

            register_case = unlogged_cases.register_client
            created = register_case.execute(username, password)
            if created:
                io.print("Your account has been successfully created!")
            else:
                io.print("Account already exists. Try another username.")

        elif choice == "3":
            break
