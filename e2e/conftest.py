import os
import time
import urllib.error
import urllib.request
from typing import Callable, Iterator

import pytest
from playwright.sync_api import Browser, Page
from testcontainers.core.container import DockerContainer
from testcontainers.core.image import DockerImage

from e2e.bank_site import BankSite

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_PORT = 8080
STARTUP_TIMEOUT_SECONDS = 30
BROWSER_TIMEOUT_MILLISECONDS = 5000


class WebApp:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def url(self, path: str) -> str:
        return f"{self.base_url}{path}"


@pytest.fixture(scope="session")
def app_image() -> Iterator[str]:
    """The application image. Set APP_IMAGE to reuse an image built
    beforehand (e.g. `docker build -t login-senha-ryan .`); otherwise it
    is built from the project's Dockerfile."""
    prebuilt = os.getenv("APP_IMAGE")
    if prebuilt:
        yield prebuilt
        return
    with DockerImage(path=PROJECT_ROOT, tag="login-senha-ryan:e2e") as image:
        yield str(image)


def wait_until_serving(url: str) -> None:
    deadline = time.monotonic() + STARTUP_TIMEOUT_SECONDS
    while True:
        request = urllib.request.Request(url, headers={"Connection": "close"})
        try:
            with urllib.request.urlopen(request, timeout=2):
                return
        except urllib.error.HTTPError:
            return
        except OSError:
            if time.monotonic() > deadline:
                raise
            time.sleep(0.2)


@pytest.fixture
def web_app(app_image, database, docker_network) -> Iterator[WebApp]:
    """The application running from its image against a freshly migrated
    database, reachable over HTTP like in production."""
    container = DockerContainer(app_image)
    container.with_network(docker_network)
    container.with_env("DB_STRING_CONNECTION", database.network_dsn)
    container.with_exposed_ports(APP_PORT)
    with container:
        host = container.get_container_host_ip()
        port = container.get_exposed_port(APP_PORT)
        app = WebApp(f"http://{host}:{port}")
        wait_until_serving(app.url("/"))
        yield app


@pytest.fixture
def page(page: Page) -> Page:
    page.set_default_timeout(BROWSER_TIMEOUT_MILLISECONDS)
    return page


@pytest.fixture
def new_site(browser: Browser, web_app) -> Iterator[Callable[[], BankSite]]:
    """Opens the bank site in a new, independent browser session (its own
    cookies), so a test can play several people.

    The server handles one connection at a time (#96): an idle keep-alive
    connection from one browser blocks every other one. Until that is
    fixed, a person must leave() before the next one acts."""
    contexts = []

    def open_site() -> BankSite:
        context = browser.new_context()
        contexts.append(context)
        page = context.new_page()
        page.set_default_timeout(BROWSER_TIMEOUT_MILLISECONDS)
        return BankSite(page, web_app)

    yield open_site
    for context in contexts:
        context.close()
