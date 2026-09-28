import os
import re
import subprocess

import pytest

ROOT = os.path.dirname(os.path.abspath(__file__))
COMMITTED_CREDENTIALS = "credentials are committed to the repository (#99)"


def tracked_files() -> list[str]:
    return subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True,
        check=True
    ).stdout.split()


def read(path: str) -> str:
    with open(os.path.join(ROOT, path), encoding="utf-8",
              errors="ignore") as file:
        return file.read()


@pytest.mark.xfail(strict=True, raises=AssertionError,
                   reason=COMMITTED_CREDENTIALS)
def test_no_environment_file_is_versioned():
    assert ".env" not in tracked_files()
    assert ".env" in read(".gitignore").split()


@pytest.mark.xfail(strict=True, raises=AssertionError,
                   reason=COMMITTED_CREDENTIALS)
def test_no_database_password_is_versioned():
    configuration = [path for path in tracked_files()
                     if not path.endswith(".py")]
    leaking = [path for path in configuration
               if re.search(r"(PASSWORD:\s*\w|://\w+:\w+@|password=\w)",
                            read(path))]
    assert leaking == []


@pytest.mark.xfail(strict=True, raises=AssertionError,
                   reason=COMMITTED_CREDENTIALS)
def test_the_database_is_only_published_on_localhost():
    published = re.findall(r'-\s*"([^"]*:5432)"', read("docker-compose.yml"))
    assert published and all(port.startswith("127.0.0.1:")
                             for port in published)
