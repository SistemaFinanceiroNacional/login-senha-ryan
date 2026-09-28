-- Rolling back would delete every passkey, locking their clients out, and
-- clients without a password cannot satisfy NOT NULL again. Refuse
-- instead of losing them.
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM passkeys)
       OR EXISTS (SELECT 1 FROM clients WHERE password IS NULL) THEN
        RAISE EXCEPTION 'rolling back would delete passkeys of registered '
                        'clients';
    END IF;
END
$$;

DROP TABLE webauthn_ceremonies;
DROP TABLE passkeys;
ALTER TABLE clients ALTER COLUMN password SET NOT NULL;
