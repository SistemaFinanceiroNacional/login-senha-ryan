from Infrastructure.authServiceDB import AuthServiceDB
from fake_config.fakes import (
    fake_context,
    fake_connection,
    fake_identity
)
from maybe import isNothing


def test_login_with_no_password():
    identifier = fake_identity(1)
    conn = fake_connection()
    cntx = fake_context()
    auth = AuthServiceDB(cntx, conn, identifier)

    assert isNothing(auth.authenticate('ryan', ''))


def test_no_login():
    identifier = fake_identity(1)
    conn = fake_connection()
    cntx = fake_context()
    auth = AuthServiceDB(cntx, conn, identifier)

    assert isNothing(auth.authenticate('', 'abc123'))
