from threading import Thread
from time import sleep

import pytest

from ApplicationService import connection_pool
from fake_config.fakes import fake_identity, fake_connection, fake_cursor


@pytest.mark.psql_conn_pool
def test_two_different_identities_returning_two_different_connections():
    psql_conn = connection_pool.postgresql_connection_pool(fake_connection, 2)
    id1 = fake_identity(141)
    id2 = fake_identity(555)

    connection_id1 = psql_conn.get_connection(id1)
    connection_id2 = psql_conn.get_connection(id2)

    assert connection_id1 != connection_id2


@pytest.mark.psql_conn_pool
def test_one_id_returning_the_same_connection_obj():
    psql_conn = connection_pool.postgresql_connection_pool(fake_connection)
    id1 = fake_identity(141)

    connection_id1 = psql_conn.get_connection(id1)
    second_connection_id1 = psql_conn.get_connection(id1)

    assert connection_id1 == second_connection_id1


@pytest.mark.psql_conn_pool
def test_verifying_cursor_class():
    psql_conn = connection_pool.postgresql_connection_pool(fake_connection)

    id1 = fake_identity(141)

    cursor_id1 = psql_conn.get_cursor(id1)

    assert isinstance(cursor_id1, fake_cursor)


@pytest.mark.psql_conn_pool
def test_obtaining_the_cursor():
    psql_conn = connection_pool.postgresql_connection_pool(fake_connection)

    id1 = fake_identity(141)

    cursor_id1 = psql_conn.get_cursor(id1)
    second_cursor_id1 = psql_conn.get_cursor(id1)

    assert cursor_id1 == second_cursor_id1


@pytest.mark.psql_conn_pool
def test_accessing_connections_tuple():
    psql_conn = connection_pool.postgresql_connection_pool(fake_connection)

    id1 = fake_identity(141)

    psql_conn.get_connection(id1)

    assert isinstance(psql_conn.used_connections[id1.value()], tuple)


@pytest.mark.psql_conn_pool
def test_verifying_if_the_second_tuple_item_is_not_none():
    psql_conn = connection_pool.postgresql_connection_pool(fake_connection)

    id1 = fake_identity(141)

    psql_conn.get_connection(id1)

    assert psql_conn.used_connections[id1.value()][1] is not None


@pytest.mark.psql_conn_pool
def test_refund_same_connection():
    psql_pool = connection_pool.postgresql_connection_pool(fake_connection)
    id1 = fake_identity(141)
    conn1 = psql_pool.get_connection(id1)

    psql_pool.refund(id1)
    id2 = fake_identity(500)
    conn2 = psql_pool.get_connection(id2)

    assert conn1 == conn2


@pytest.mark.psql_conn_pool
def test_trying_to_create_conn_but_max_has_reached():
    psql_conn = connection_pool.postgresql_connection_pool(fake_connection)
    id1 = fake_identity(141)
    id2 = fake_identity(555)

    def get_conn(id_conn):
        return psql_conn.get_connection(id_conn)

    thread1 = Thread(target=get_conn, args=(id1,))
    print("Task1 created")
    thread1.start()

    sleep(1)

    thread2 = Thread(target=get_conn, args=(id2,))
    print("Task2 created")
    thread2.start()

    sleep(2)

    print("Going for if's...")
    if not thread1.is_alive():
        print("Thread1 is done")

        assert thread2.is_alive()
        print("Thread2 is not done")

        psql_conn.refund(id1)
        print("Thread1 refunded!!!")
        sleep(2)

        assert not thread2.is_alive()

    elif not thread2.is_alive():
        print("Thread2 is done")

        assert thread1.is_alive()
        print("Thread1 is not done")

        psql_conn.refund(id2)
        print("Task2 refunded!!!")
        sleep(2)

        assert not thread1.is_alive()

    thread1.join()
    thread2.join()
