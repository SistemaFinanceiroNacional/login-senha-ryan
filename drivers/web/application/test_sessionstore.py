from datetime import timedelta

import pytest

from drivers.web.application.sessionstore import DBSessionStore
from infrastructure.connection_pool import (
    PostgresqlConnectionPool,
    psycopg2_create_connection
)
from infrastructure.dbtransactioncontext import DBTransactionContext
from infrastructure.threadIdentity import ThreadIdentity
from maybe import is_nothing

NOT_IMPLEMENTED = "server-side sessions not implemented yet (issue #94)"

pytestmark = [
    pytest.mark.integration,
    pytest.mark.xfail(strict=True, reason=NOT_IMPLEMENTED,
                      raises=NotImplementedError),
]

TOKEN = "a-random-token"


def store(idle=timedelta(minutes=30), lifetime=timedelta(hours=12)):
    pool = PostgresqlConnectionPool(psycopg2_create_connection, 1)
    identity = ThreadIdentity()
    return DBSessionStore(DBTransactionContext(pool, identity), pool,
                          identity, idle, lifetime)


def test_a_saved_session_is_loaded(database):
    sessions = store()

    sessions.save(TOKEN, {"client_id": 1, "login": "alice"})

    assert sessions.load(TOKEN).or_else(dict) == \
        {"client_id": 1, "login": "alice"}


def test_saving_again_replaces_the_data(database):
    sessions = store()
    sessions.save(TOKEN, {"login": "alice"})

    sessions.save(TOKEN, {"login": "alice", "account_id": 2})

    assert sessions.load(TOKEN).or_else(dict) == \
        {"login": "alice", "account_id": 2}


def test_unknown_and_deleted_sessions_are_not_loaded(database):
    sessions = store()
    sessions.save(TOKEN, {"login": "alice"})

    sessions.delete(TOKEN)

    assert is_nothing(sessions.load(TOKEN))
    assert is_nothing(sessions.load("never-issued"))


def test_idle_sessions_expire(database):
    sessions = store(idle=timedelta(0))
    sessions.save(TOKEN, {"login": "alice"})

    assert is_nothing(sessions.load(TOKEN))


def test_sessions_expire_after_their_lifetime_even_when_active(database):
    sessions = store(lifetime=timedelta(0))
    sessions.save(TOKEN, {"login": "alice"})

    assert is_nothing(sessions.load(TOKEN))


def test_tokens_are_not_stored_in_clear(database):
    store().save(TOKEN, {"login": "alice"})

    stored = database.execute("SELECT token_hash FROM sessions;")

    assert TOKEN.encode() not in [bytes(token) for (token,) in stored]
