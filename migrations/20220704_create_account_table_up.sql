CREATE TABLE IF NOT EXISTS accounts (id INT GENERATED ALWAYS
AS IDENTITY PRIMARY KEY, login text NOT NULL, password text NOT NULL, balance INT DEFAULT 0);
CREATE TABLE IF NOT EXISTS migrations_applied(id SERIAL PRIMARY KEY, version CHAR(8));
INSERT INTO migrations_applied (version) VALUES ('20220704');