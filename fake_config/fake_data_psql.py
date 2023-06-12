from faker import Faker
import random
import psycopg2
from password import Password as passW

fake = Faker()


def generate_clients(num_clients):
    clients = []
    for _ in range(num_clients):
        login = fake.user_name()
        password = 'abc123'
        clients.append((login, str(passW(password))))
    return clients


def generate_accounts(num_clients):
    accounts = [x for x in range(1, num_clients+1)]
    return accounts


def generate_transactions(num_transactions, num_accounts):
    transactions = []
    for _ in range(num_transactions):
        uuid = fake.uuid4()
        debit_account = random.randint(1, num_accounts)
        credit_account = random.randint(1, num_accounts)
        value = random.uniform(10.0, 1000.0)
        date = fake.date_time_between(start_date='-1y', end_date='now')
        transactions.append((uuid, debit_account, credit_account, value, date))
    return transactions


conn = psycopg2.connect(
    host="localhost",
    database="test",
    user="ryanbanco",
    password="abc123"
)

cursor = conn.Cursor()

num_clients = 10
num_transactions = 50

clients_data = generate_clients(num_clients)
accounts_data = generate_accounts(num_clients)
transactions_data = generate_transactions(num_transactions, num_clients)

cursor.executemany("INSERT INTO clients (login, password) "
                   "VALUES (%s, %s)",
                   clients_data
                   )
cursor.executemany("INSERT INTO accounts "
                   "VALUES (default)",
                   accounts_data
                   )

cursor.executemany("INSERT INTO clients_accounts (client_id, account_id) "
                   "VALUES (%s, %s)",
                   [(x, x) for x in accounts_data]
                   )

cursor.executemany("INSERT INTO transactions ("
                   "uuid, "
                   "debit_account, "
                   "credit_account, "
                   "value, "
                   "date) "
                   "VALUES (%s, %s, %s, %s, %s)", transactions_data
                   )

conn.commit()

cursor.close()
conn.close()
