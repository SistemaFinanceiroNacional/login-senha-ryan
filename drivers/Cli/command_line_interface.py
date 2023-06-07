import logging
from Domain.account import (
    insufficientFundsException,
    invalidValueToTransfer
)
from inputIO.inputIO import inputIO
from ApplicationService.unloggedUseCases import UnloggedUseCases
from ApplicationService.loggedUseCases import LoggedUseCases
from ApplicationService.contexterrors.accountdoesnotexistserror import (
    AccountDoesNotExistsError
)
from Infrastructure.authserviceinterface import AuthServiceInterface

logger = logging.getLogger("drivers.Cli.command_line_interface")
accountID = int


def transfer_money(userIO, acc_id, l_cases):
    destinationAccount = int(userIO.input(
        "Enter the ID of the destination account: "
    ))
    value = int(userIO.input("How much do you want to transfer? "))
    try:
        l_cases.transfer.execute(acc_id, destinationAccount, value)
        userIO.print("Successful transaction.")
    except insufficientFundsException:
        userIO.print("Insufficient funds.")
    except invalidValueToTransfer as e:
        userIO.print(f"{e.value} is a non-positive value to transfer.")
    except AccountDoesNotExistsError:
        userIO.print("Invalid Account ID.")


def show_transactions(userIO, acc_id, l_cases):
    transactions = l_cases.get_transactions.execute(acc_id)
    if transactions:
        for t in transactions:
            userIO.print(str(t))
    else:
        userIO.print("No transactions to show.")


def accounts_repl(userIO: inputIO, acc_id: accountID, l_cases: LoggedUseCases):
    balance_case = l_cases.get_balance
    options = {
        "1": lambda: userIO.print(f"R${balance_case.execute(acc_id):.2f}"),
        "2": lambda: transfer_money(userIO, acc_id, l_cases),
        "3": lambda: show_transactions(userIO, acc_id, l_cases),
        "4": None
    }
    userIO.print("""
            (1) Balance
            (2) Transfer money
            (3) Extract
            (4) Exit account
        """)
    while True:
        command = userIO.input("->")
        if command in options:
            action = options[command]
            if command == "4":
                break
            action()


def repl(userIO: inputIO, c_id: int, logged_cases: LoggedUseCases):
    userIO.print("""
            (1) Select account
            (2) Logout
    """)
    while True:
        command = userIO.input("->")
        if command == "1":
            accs = list(logged_cases.get_accounts.execute(c_id))
            for acc in accs:
                print(f"Account ID: {acc}")
            select_acc = int(userIO.input("Choose one ID: "))
            if select_acc in accs:
                accounts_repl(userIO, select_acc, logged_cases)
                userIO.print("""
            (1) Select account
            (2) Logout
                    """)
        elif command == "2":
            break


def main(userIO: inputIO,
         auth_service: AuthServiceInterface,
         unlogged_cases: UnloggedUseCases,
         logged_cases: LoggedUseCases
         ):

    while True:
        choice = userIO.input("Would you like to Sign In (1),"
                              " Create a new client account (2)"
                              " or Exit(3)? ")
        if choice == "1":
            username = userIO.input("Enter your username: ")
            password = userIO.inputoccult("Enter your password: ")
            if not username or not password:
                userIO.print("Login and password should not be empty.")
            else:
                logger.debug("Going to verify the account...")
                maybe_client_id = auth_service.authenticate(username, password)
                maybe_client_id.map(lambda client_id: repl(
                    userIO, client_id, logged_cases
                )).orElse(lambda: userIO.print("You are not logged in!"))

        elif choice == "2":
            username = userIO.input("Enter your new username: ")
            password = userIO.inputoccult("Enter your new password: ")
            if not username or not password:
                userIO.print("Login and password should not be empty.")

            register_case = unlogged_cases.register_client
            created = register_case.execute(username, password)
            if created:
                userIO.print("Your account has been successfully created!")
            else:
                userIO.print("Account already exists. Try another username.")

        elif choice == "3":
            break
