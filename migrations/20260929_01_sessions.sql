-- depends: 20260928_02_passkeys

-- Server-side sessions (issue #94). The browser only holds a random
-- token; the session data lives here, keyed by the token's SHA-256 so a
-- leaked table does not hand out live sessions.
--
-- Sessions are disposable: rolling this migration back drops them, which
-- signs everybody out but loses no business data.

CREATE TABLE sessions (
    token_hash BYTEA PRIMARY KEY,
    data JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX sessions_expires_at ON sessions (expires_at);
