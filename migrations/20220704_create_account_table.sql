CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    login text NOT NULL UNIQUE,
    password text NOT NULL
);

CREATE TABLE IF NOT EXISTS accounts (
    id SERIAL PRIMARY KEY,
    client_id INT,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

CREATE TABLE IF NOT EXISTS transactions (
    uuid UUID PRIMARY KEY,
    debit_account INT NOT NULL,
    credit_account INT NOT NULL,
    value FLOAT NOT NULL,
    date TIMESTAMP NOT NULL,
    FOREIGN KEY (debit_account) REFERENCES accounts(id),
    FOREIGN KEY (credit_account) REFERENCES accounts(id)
);