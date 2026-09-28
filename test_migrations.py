import pytest

APPLICATION_TABLES = {
    "clients", "accounts", "clients_accounts", "transactions"
}


@pytest.mark.integration
def test_migrations_can_be_rolled_back_and_reapplied(database):
    database.rollback_all_migrations()
    assert APPLICATION_TABLES.isdisjoint(database.table_names())

    database.apply_all_migrations()
    assert APPLICATION_TABLES <= database.table_names()
