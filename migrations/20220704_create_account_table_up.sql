CREATE TABLE IF NOT EXISTS accounts (id INT GENERATED ALWAYS
AS IDENTITY PRIMARY KEY, login text NOT NULL, password text NOT NULL, balance INT DEFAULT 0);