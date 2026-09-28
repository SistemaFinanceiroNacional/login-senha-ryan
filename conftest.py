import os
from typing import Iterator

import psycopg2
import pytest
from testcontainers.community.postgres import PostgresContainer
from testcontainers.core.network import Network
from yoyo import get_backend, read_migrations  # type: ignore[import]

from testsupport.bank import Bank

MIGRATIONS_PATH = os.path.join(os.path.dirname(__file__), "migrations")
POSTGRES_IMAGE = "postgres:16-alpine"
POSTGRES_ALIAS = "db"
POSTGRES_PORT = 5432


class Database:
    def __init__(self, container: PostgresContainer):
        user = container.username
        password = container.password
        dbname = container.dbname
        credentials = f"dbname={dbname} user={user} password={password}"

        host = container.get_container_host_ip()
        port = container.get_exposed_port(POSTGRES_PORT)
        self.dsn = f"{credentials} host={host} port={port}"
        self.network_dsn = (
            f"{credentials} host={POSTGRES_ALIAS} port={POSTGRES_PORT}"
        )
        self._url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

    def apply_all_migrations(self) -> None:
        backend = get_backend(self._url)
        migrations = read_migrations(MIGRATIONS_PATH)
        with backend.lock():
            backend.apply_migrations(backend.to_apply(migrations))

    def rollback_all_migrations(self) -> None:
        self._rollback(lambda applied: applied)

    def rollback_down_to(self, migration_id: str) -> None:
        """Rolls back the given migration and every later one."""
        def down_to(applied):
            ids = [migration.id for migration in applied]
            return applied[:ids.index(migration_id) + 1]
        self._rollback(down_to)

    def _rollback(self, choose) -> None:
        backend = get_backend(self._url)
        migrations = read_migrations(MIGRATIONS_PATH)
        with backend.lock():
            applied = backend.to_rollback(migrations)
            backend.rollback_migrations(choose(applied))

    def reset(self) -> None:
        """Drops everything, migrations bookkeeping included."""
        self.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")

    def execute(self, query: str, params: tuple = ()) -> list[tuple]:
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if cursor.description is None:
                    return []
                return cursor.fetchall()

    def table_names(self) -> set[str]:
        rows = self.execute(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema = 'public';"
        )
        return {name for (name,) in rows}


@pytest.fixture(scope="session")
def docker_network() -> Iterator[Network]:
    with Network() as network:
        yield network


@pytest.fixture(scope="session")
def postgres_container(docker_network) -> Iterator[PostgresContainer]:
    container = PostgresContainer(POSTGRES_IMAGE, driver=None)
    container.with_network(docker_network)
    container.with_network_aliases(POSTGRES_ALIAS)
    with container:
        yield container


@pytest.fixture
def database(postgres_container, monkeypatch) -> Iterator[Database]:
    """A freshly migrated database, exposed to the application through
    DB_STRING_CONNECTION exactly as in production."""
    db = Database(postgres_container)
    db.reset()
    db.apply_all_migrations()
    monkeypatch.setenv("DB_STRING_CONNECTION", db.dsn)
    yield db


@pytest.fixture
def bank(database) -> Bank:
    """The use cases wired to the real infrastructure and database."""
    return Bank()
