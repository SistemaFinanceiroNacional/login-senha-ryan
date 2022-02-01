import getpass
import hashlib

login = input("Informe o usuário: ")
senha = getpass.getpass("Informe a senha: ")

hash_senha = hashlib.sha512(senha.encode("utf-8"))
righthash = hashlib.sha512("abc123".encode("utf-8"))

if login == "pedro" and hash_senha.digest() == righthash.digest():
    print("Você está logado.")

else:
    print("Usuário negado.")
