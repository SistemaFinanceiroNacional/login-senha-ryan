from ApplicationService.internalAccount import internalAccount, insufficientFundsException, invalidValueToTransfer
import password
import logging
from inputIO.inputIO import inputIO
from ApplicationService.loginUseCase import loginUseCase
from ApplicationService.transferFundsBetweenAccountsUseCase import transferFundsBetweenAccountsUseCase
from ApplicationService.openAccountUseCase import openAccountUseCase

logger = logging.getLogger("drivers.Cli.command_line_interface")

def repl(userIO: inputIO, acc: internalAccount, transfer_use_case: transferFundsBetweenAccountsUseCase):
    comando = ""
    while comando != "logout":
        comando = userIO.input("->")
        if comando == "balance":
            userIO.print(acc.balance())
        elif comando == "transfer":
            destinationAccount = userIO.input("Enter the destination account: ")
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
         transfer_use_case: transferFundsBetweenAccountsUseCase,
         open_account_use_case: openAccountUseCase):

    choose = userIO.input("Would you like to Sign In (1) or Create a new account (2)? ")
    if choose == "1":
        login = userIO.input("Enter your username: ")
        senha = password.password(userIO.inputoccult("Enter your password: "))
        logger.debug("Going to verify the account...")
        possible_account = login_use_case.execute(login, senha)
        possible_account.map(lambda acc: repl(userIO, acc, transfer_use_case)).orElse(lambda: userIO.print("You are not logged in!"))

    elif choose == "2":
        loginFromUser = userIO.input("Enter your new username: ")
        passwordFromUser = password.password(userIO.inputoccult("Enter your new password: "))
        if open_account_use_case.execute(loginFromUser, passwordFromUser):
            userIO.print("Your account has been successfully created!")
        else:
            userIO.print("Account already exists. Try another username.")
