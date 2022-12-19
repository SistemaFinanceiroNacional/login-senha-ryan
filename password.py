import hashlib

class password:
    def __init__(self,password):
        self.password = password

    def __str__(self):
        hash_password = hashlib.sha512(self.password.encode("utf-8"))
        return hash_password.hexdigest()