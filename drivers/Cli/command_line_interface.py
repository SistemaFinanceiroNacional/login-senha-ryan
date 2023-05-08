from ApplicationService.internal_account import (
    internalAccount as ia,
    insufficientFundsException,
    invalidValueToTransfer
)
from password import password as pw
import logging
from inputIO.inputIO import inputIO
from ApplicationService.loginUseCase import loginUseCase
from ApplicationService.transferFundsUseCase import transferFundsUseCase
from ApplicationService.openAccountUseCase import openAccountUseCase

logger = logging.getLogger("drivers.Cli.command_line_interface")


def repl(userIO: inputIO, acc: ia, transfer_use_case: transferFundsUseCase):
    comando = ""
    while comando != "logout":
        comando = userIO.input("->")
        if comando == "balance":
            userIO.print(acc.get_balance())
        elif comando == "transfer":
            destinationAccount = userIO.input(
                "Enter the destination account: "
            )
            value = int(userIO.input("How much do you want to transfer? "))
            try:
                transfer_use_case.execute(acc, destinationAccount, value)
                userIO.print("Successful transaction.")
            except insufficientFundsException:
                userIO.print("Insufficient funds.")
            except invalidValueToTransfer as e:
                userIO.print(f"{e.value} is a non-positive value to transfer.")


def main(userIO: inputIO,
         login_use_case: loginUseCase,
         transfer_use_case: transferFundsUseCase,
         open_account_use_case: openAccountUseCase):

    while True:
        choice = userIO.input("Would you like to Sign In (1),"
                              " Create a new account (2)"
                              " or Exit(3)? ")
        if choice == "1":
            login = userIO.input("Enter your username: ")
            senha = pw(userIO.inputoccult("Enter your password: "))
            logger.debug("Going to verify the account...")
            possible_account = login_use_case.execute(login, senha)
            possible_account.map(lambda acc: repl(
                userIO, acc, transfer_use_case
            )).orElse(lambda: userIO.print("You are not logged in!"))

        elif choice == "2":
            user_login = userIO.input("Enter your new username: ")
            user_password = userIO.inputoccult("Enter your new password: ")
            if not user_login or not user_password:
                userIO.print("Login and password should not be empty.")
            elif open_account_use_case.execute(user_login, user_password):
                userIO.print("Your account has been successfully created!")
            else:
                userIO.print("Account already exists. Try another username.")

        elif choice == "3":
            break
