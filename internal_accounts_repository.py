import maybe
import internalAccount

class internal_accounts_repository:
    def __init__(self, connection_pool, identifier):
        self.connection_pool = connection_pool
        self.identifier = identifier

    def add_account(self, new_login, new_password):
        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute("SELECT * FROM accounts WHERE login = %s ", (new_login,))
        account_query_result = cursor.fetchone()

        if not account_query_result:
            cursor.execute("INSERT INTO accounts (login,password,balance) VALUES (%s,%s,%s)", (new_login, str(new_password), 0))

        return not account_query_result

    def authentication(self, login, password):
        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute("SELECT login, password, balance FROM accounts WHERE login=%s AND password=%s", (login, str(password)))
        find_login_list = cursor.fetchone()
        if find_login_list is not None:
            return maybe.just(internalAccount.internalAccount(find_login_list[0], find_login_list[1], find_login_list[2]))
        return maybe.nothing()

    def updateBalance(self, login, new_balance):
        cursor = self.connection_pool.get_cursor(self.identifier)
        cursor.execute("UPDATE accounts SET balance=%s WHERE login=%s", (new_balance, login))
