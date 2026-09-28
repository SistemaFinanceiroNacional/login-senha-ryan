import psycopg2
import pytest

from domain.amount import Amount
from domain.money import Money

APPLICATION_TABLES = {
    "clients", "accounts", "clients_accounts", "transactions"
}
BANK_DEPOSITS_ACCOUNT = 1


@pytest.mark.integration
def test_migrations_can_be_rolled_back_and_reapplied(database):
    database.rollback_all_migrations()
    assert APPLICATION_TABLES.isdisjoint(database.table_names())

    database.apply_all_migrations()
    assert APPLICATION_TABLES <= database.table_names()


# Compatibility with the previous version of the application (#116). The
# SQL below is what that version runs: it reads `SELECT t.*` from
# transactions and writes only the FLOAT column.

def written_by_previous_version(database, account_id, value) -> None:
    database.execute(
        "INSERT INTO transactions "
        "(uuid, debit_account, credit_account, value, date) "
        "VALUES (gen_random_uuid(), %s, %s, %s, now());",
        (BANK_DEPOSITS_ACCOUNT, account_id, value)
    )


def balance(bank, client) -> Money:
    return bank.get_balance.execute(client.id, client.account)\
        .or_else_throw(AssertionError("no balance"))


@pytest.mark.integration
def test_transactions_keep_the_shape_the_previous_version_reads(database):
    columns = database.execute(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_name = 'transactions' ORDER BY ordinal_position;"
    )

    assert [name for (name,) in columns] == [
        "uuid", "debit_account", "credit_account", "value", "date"
    ]


@pytest.mark.integration
def test_rows_written_by_the_previous_version_are_read_exactly(
        database, bank
):
    alice = bank.open_client("alice")

    for _ in range(3):
        written_by_previous_version(database, alice.account, 0.1)

    assert balance(bank, alice) == Money("0.30")


@pytest.mark.integration
def test_rolling_back_and_forward_keeps_every_amount(database, bank):
    alice = bank.open_client("alice")
    for value in ["0.10", "0.10", "0.10", "150.50"]:
        assert bank.deposit.execute(alice.id, alice.account, Amount(value))

    database.rollback_last_migration()
    database.apply_all_migrations()

    assert balance(bank, alice) == Money("150.80")


@pytest.mark.integration
def test_rolling_back_refuses_to_lose_cents(database, bank):
    alice = bank.open_client("alice")
    large = Amount("1234567890123456.78")
    assert bank.deposit.execute(alice.id, alice.account, large)

    with pytest.raises(psycopg2.Error, match="would lose cents"):
        database.rollback_last_migration()

    assert balance(bank, alice) == large
