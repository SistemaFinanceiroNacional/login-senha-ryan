import contas
import inputIO
import password
import psycopg2

def repl(userIO,acc):
    comando = ""
    while comando != "sair":
        comando = userIO.input("->")
        if comando == "saldo":
            userIO.print(acc.saldo())


def main(contas,userIO):
    choose = userIO.input("Deseja fazer login (1) ou cadastro (2)? ")
    if choose == "1":
        login = userIO.input("Informe o usuário: ")
        senha = password.password(userIO.inputoccult("Informe a senha: "))
        possible_account = contas.authentication(login,senha)
        possible_account.map(lambda acc: repl(userIO,acc)).orElse(lambda : userIO.print("Você não está logado!"))


    elif choose == "2":
        login = userIO.input("Informe o seu novo usuário: ")
        senha = password.password(userIO.inputoccult("Informe a sua nova senha: "))
        if contas.add_account(login,senha):
            userIO.print("Conta criada com sucesso!")
        else:
            userIO.print("Conta já existe. Tente outro usuário e senha.")


if __name__ == "__main__":
    with psycopg2.connect("dbname=ryanbanco user=ryanbanco password=abc123") as connection, connection.cursor() as cursor, contas.contas(cursor) as c:
        main(c,inputIO.inputIO())
