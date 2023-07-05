from infrastructure.authservicedb import AuthServiceDB
from fake_config.fakes import (
    FakeContext,
    FakeConnectionPool,
    FakeIdentity
)
from maybe import is_nothing


def test_login_with_no_password():
    identifier = FakeIdentity(1)
    conn = FakeConnectionPool()
    cntx = FakeContext()
    auth = AuthServiceDB(cntx, conn, identifier)

    assert is_nothing(auth.authenticate('ryan', ''))


def test_no_login():
    identifier = FakeIdentity(1)
    conn = FakeConnectionPool()
    cntx = FakeContext()
    auth = AuthServiceDB(cntx, conn, identifier)

    assert is_nothing(auth.authenticate('', 'abc123'))
