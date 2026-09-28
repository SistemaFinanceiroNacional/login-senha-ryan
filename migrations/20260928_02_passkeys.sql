-- depends: 20260928_01_exact_transaction_amounts

-- Passwordless authentication with FIDO2/WebAuthn (issue #119), expand
-- step.
--
-- Clients registered with a passkey have no password. Previous versions
-- keep working on this schema: they insert clients with a password and
-- authenticate by login and password, which simply never matches a
-- passkey-only client.

ALTER TABLE clients ALTER COLUMN password DROP NOT NULL;

CREATE TABLE passkeys (
    credential_id BYTEA PRIMARY KEY,
    client_id INT NOT NULL REFERENCES clients (id),
    user_handle BYTEA NOT NULL,
    public_key BYTEA NOT NULL,
    sign_count BIGINT NOT NULL CHECK (sign_count >= 0),
    transports TEXT[] NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX passkeys_client_id ON passkeys (client_id);

-- Challenges of registrations and authentications in progress. They are
-- kept on the server (never in the client-side session, which can be
-- forged, see #94) and consumed on first use.
CREATE TABLE webauthn_ceremonies (
    id UUID PRIMARY KEY,
    kind TEXT NOT NULL CHECK (kind IN ('registration', 'authentication')),
    login TEXT NOT NULL,
    challenge BYTEA NOT NULL,
    user_handle BYTEA,
    expires_at TIMESTAMPTZ NOT NULL
);
