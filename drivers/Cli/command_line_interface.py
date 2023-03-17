import internal_accounts_repository
import external_accounts_interactions
from inputIO import inputIO
import internalAccount
import password
import psycopg2
from ApplicationService import transferFundsBetweenAccounts


def repl(userIO, acc, transfer_use_case):
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
            except internalAccount.insufficientFundsException:
                userIO.print("Insufficient funds.")
            except internalAccount.invalidValueToTransfer as e:
                userIO.print(f"{e.value} is a non-positive value to transfer.")


def main(accounts_repository, transfer_use_case, userIO):
    choose = userIO.input("Would you like to Sign In (1) or Create a new account (2)? ")
    if choose == "1":
        login = userIO.input("Enter your username: ")
        senha = password.password(userIO.inputoccult("Enter your password: "))
        possible_account = accounts_repository.authentication(login, senha)
        possible_account.map(lambda acc: repl(userIO, acc, transfer_use_case)).orElse(lambda: userIO.print("You are not logged in!"))

    elif choose == "2":
        loginFromUser = userIO.input("Enter your new username: ")
        passwordFromUser = password.password(userIO.inputoccult("Enter your new password: "))
        if accounts_repository.add_account(loginFromUser, passwordFromUser):
            userIO.print("Your account has been successfully created!")
        else:
            userIO.print("Account already exists. Try another username and password.")
