from ApplicationService import connection_pool, identity

class fake_identity(identity.identity):
    def __init__(self, iden):
        self.iden = iden

    def value(self):
        return self.iden

class fake_connection:
    def cursor(self):
        return fake_cursor()

class fake_cursor:
    pass


def test_connection_pool_postgresql_with_two_different_identities_returning_two_different_connections():
    psql_conn = connection_pool.postgresql_connection_pool(fake_connection, 2)
    id1 = fake_identity(141)
    id2 = fake_identity(555)

    connection_id1 = psql_conn.get_connection(id1)
    connection_id2 = psql_conn.get_connection(id2)

    assert connection_id1 != connection_id2

def test_connection_pool_postgresql_with_one_id_returning_the_same_connection_obj():
    psql_conn = connection_pool.postgresql_connection_pool(fake_connection)
    id1 = fake_identity(141)

    connection_id1 = psql_conn.get_connection(id1)
    second_connection_id1 = psql_conn.get_connection(id1)

    assert connection_id1 == second_connection_id1

def test_connection_pool_postgresql_verifying_cursor_class():
    psql_conn = connection_pool.postgresql_connection_pool(fake_connection)

    id1 = fake_identity(141)

    cursor_id1 = psql_conn.get_cursor(id1)

    assert isinstance(cursor_id1, fake_cursor)

def test_connection_pool_postgresql_obtaining_the_cursor():
    psql_conn = connection_pool.postgresql_connection_pool(fake_connection)

    id1 = fake_identity(141)

    cursor_id1 = psql_conn.get_cursor(id1)
    second_cursor_id1 = psql_conn.get_cursor(id1)

    assert cursor_id1 == second_cursor_id1

def test_connection_pool_postgresql_accessing_connections_tuple():
    psql_conn = connection_pool.postgresql_connection_pool(fake_connection)

    id1 = fake_identity(141)

    psql_conn.get_connection(id1)

    assert isinstance(psql_conn.connections[id1.value()], tuple)

def test_connection_pool_postgresql_verifying_if_the_second_tuple_item_is_not_none():
    psql_conn = connection_pool.postgresql_connection_pool(fake_connection)

    id1 = fake_identity(141)

    psql_conn.get_connection(id1)

    assert psql_conn.connections[id1.value()][1] is not None

def test_connection_pool_refund_same_connection():
    psql_conn_pool = connection_pool.postgresql_connection_pool(fake_connection)
    id1 = fake_identity(141)
    conn1 = psql_conn_pool.get_connection(id1)

    psql_conn_pool.refund(id1)
    id2 = fake_identity(500)
    conn2 = psql_conn_pool.get_connection(id2)

    assert conn1 == conn2

def test_connection_pool_refund_trying_to_create_conn_but_max_has_reached():
    psql_conn = connection_pool.postgresql_connection_pool(fake_connection)
    id1 = fake_identity(141)
    id2 = fake_identity(555)

    connection_id1 = psql_conn.get_connection(id1)
    connection_id2 = psql_conn.get_connection(id2)
    psql_conn.refund(id1)

