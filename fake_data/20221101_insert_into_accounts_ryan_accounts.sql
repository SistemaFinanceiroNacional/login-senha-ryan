-- accounts 'ryan' has password 'abc123'
INSERT INTO clients (login, password) VALUES ('ryan', 'c70b5dd9ebfb6f51d09d4132b7170c9d20750a7852f00680f65658f0310e810056e6763c34c9a00b0e940076f54495c169fc2302cceb312039271c43469507dc');
INSERT INTO accounts VALUES (default);
INSERT INTO clients_accounts (cliend_id, account_id) VALUES IN (
    SELECT id, id+1 FROM clients WHERE login=ryan
);