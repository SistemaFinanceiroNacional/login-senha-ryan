import hashlib


class Password:
    def __init__(self, raw_password: str):
        self.password = raw_password

    def __str__(self):
        hash_password = hashlib.sha512(self.password.encode("utf-8"))
        return hash_password.hexdigest()
