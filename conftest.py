import os
from typing import Iterator

import psycopg2
import pytest
from testcontainers.community.postgres import PostgresContainer
from testcontainers.core.network import Network
from yoyo import get_backend, read_migrations  # type: ignore[import]

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
        backend = get_backend(self._url)
        migrations = read_migrations(MIGRATIONS_PATH)
        with backend.lock():
            backend.rollback_migrations(backend.to_rollback(migrations))

    def table_names(self) -> set[str]:
        query = "SELECT table_name FROM information_schema.tables " \
                "WHERE table_schema = 'public';"
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return {name for (name,) in cursor.fetchall()}


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
    db.rollback_all_migrations()
    db.apply_all_migrations()
    monkeypatch.setenv("DB_STRING_CONNECTION", db.dsn)
    yield db
