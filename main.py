import getpass

login = input("Informe o usuário: ")
senha = getpass.getpass("Informe a senha: ")

if login == "joao" and senha == "abc123":
    print("Você está logado.")

else:
    print("Usuário negado.")
