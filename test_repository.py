import os
import re
import subprocess

import pytest

ROOT = os.path.dirname(os.path.abspath(__file__))


def tracked_files() -> list[str]:
    return subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True,
        check=True
    ).stdout.split()


def read(path: str) -> str:
    with open(os.path.join(ROOT, path), encoding="utf-8",
              errors="ignore") as file:
        return file.read()


def test_no_environment_file_is_versioned():
    assert ".env" not in tracked_files()
    assert ".env" in read(".gitignore").split()


def test_no_database_password_is_versioned():
    configuration = [path for path in tracked_files()
                     if not path.endswith(".py")]
    leaking = [path for path in configuration
               if re.search(r"(PASSWORD:\s*\w|://\w+:\w+@|password=\w)",
                            read(path))]
    assert leaking == []


def test_the_database_is_only_published_on_localhost():
    published = re.findall(r'-\s*"([^"]*:5432)"', read("docker-compose.yml"))
    assert published and all(port.startswith("127.0.0.1:")
                             for port in published)


def compose_config(environment: dict) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["docker", "compose", "--env-file", os.devnull, "config", "-q"],
        cwd=ROOT, capture_output=True, text=True,
        env={"PATH": os.environ["PATH"], **environment}
    )


@pytest.mark.integration
def test_compose_takes_the_credentials_from_the_environment():
    missing = compose_config({})
    given = compose_config({"POSTGRES_USER": "u", "POSTGRES_PASSWORD": "p",
                            "POSTGRES_DB": "d"})

    assert missing.returncode != 0
    assert re.search(r"required variable POSTGRES_(USER|PASSWORD|DB)",
                     missing.stderr)
    assert given.returncode == 0, given.stderr
