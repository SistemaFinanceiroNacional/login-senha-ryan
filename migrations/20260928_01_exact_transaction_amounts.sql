-- depends: 20220704_create_account_table

-- Expand step of moving money off FLOAT (issue #116).
--
-- The exact amount lives in a side table so that `transactions` keeps the
-- shape previous versions read with `SELECT t.*`. The application writes
-- both tables and reads the exact amount, falling back to the FLOAT
-- column for rows written by a previous version; it can therefore be
-- rolled back and forward freely. A later contract step will fold the
-- exact amount into `transactions` and drop the FLOAT column.

CREATE TABLE transaction_amounts (
    transaction_uuid UUID PRIMARY KEY
        REFERENCES transactions (uuid) ON DELETE CASCADE,
    amount NUMERIC(18, 2) NOT NULL CHECK (amount > 0)
);

INSERT INTO transaction_amounts (transaction_uuid, amount)
SELECT uuid, round(value::numeric, 2)
FROM transactions
WHERE round(value::numeric, 2) > 0;
