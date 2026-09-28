-- Dropping the exact amounts leaves the FLOAT column as the only copy of
-- each value. Refuse when that would lose cents (amounts too large for a
-- double) instead of silently corrupting balances.
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM transaction_amounts a
        JOIN transactions t ON t.uuid = a.transaction_uuid
        WHERE round(t.value::numeric, 2) <> a.amount
    ) THEN
        RAISE EXCEPTION 'rolling back would lose cents: some amounts are '
                        'not exactly representable in transactions.value';
    END IF;
END
$$;

DROP TABLE transaction_amounts;
