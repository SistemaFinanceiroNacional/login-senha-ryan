import os
import socket
import time
import urllib.error
import urllib.request
from typing import Callable, Iterator

import pytest
from playwright.sync_api import Browser, Page
from testcontainers.core.container import DockerContainer
from testcontainers.core.image import DockerImage

from e2e.authenticators import PLATFORM
from e2e.bank_site import BankSite

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_PORT = 8080
STARTUP_TIMEOUT_SECONDS = 30
BROWSER_TIMEOUT_MILLISECONDS = 5000
# Kept short so that tests about stalled connections do not wait long.
IDLE_TIMEOUT_SECONDS = 2


class WebApp:
    def __init__(self, base_url: str, container=None):
        self.base_url = base_url
        self._container = container

    def logs(self) -> str:
        """Everything the application wrote to its standard streams."""
        stdout, stderr = self._container.get_logs()
        return (stdout + stderr).decode("utf-8", errors="replace")

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


def free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


@pytest.fixture
def web_app(app_image, database, docker_network) -> Iterator[WebApp]:
    """The application running from its image against a freshly migrated
    database, reachable over HTTP like in production.

    It is served at a fixed http://localhost:<port> origin, known to the
    application beforehand: WebAuthn binds credentials to the exact
    origin (localhost is a secure context, so no TLS is needed)."""
    port = free_port()
    origin = f"http://localhost:{port}"
    container = DockerContainer(app_image)
    container.with_network(docker_network)
    container.with_env("DB_STRING_CONNECTION", database.network_dsn)
    container.with_env("WEBAUTHN_RP_ID", "localhost")
    container.with_env("WEBAUTHN_ORIGIN", origin)
    container.with_env("HTTP_IDLE_TIMEOUT_SECONDS", str(IDLE_TIMEOUT_SECONDS))
    # The most verbose logging: nothing secret may show up even then.
    container.with_env("LOG_LEVEL", "DEBUG")
    container.with_bind_ports(APP_PORT, port)
    with container:
        app = WebApp(origin, container)
        wait_until_serving(app.url("/"))
        yield app


@pytest.fixture
def page(page: Page) -> Page:
    page.set_default_timeout(BROWSER_TIMEOUT_MILLISECONDS)
    return page


@pytest.fixture
def new_site(browser: Browser,
             web_app
             ) -> Iterator[Callable[..., BankSite]]:
    """Opens the bank site in a new, independent browser session (its own
    cookies and authenticator), so a test can play several people at
    once."""
    contexts = []

    def open_site(authenticator: str = PLATFORM) -> BankSite:
        context = browser.new_context()
        contexts.append(context)
        page = context.new_page()
        page.set_default_timeout(BROWSER_TIMEOUT_MILLISECONDS)
        return BankSite(page, web_app, authenticator)

    yield open_site
    for context in contexts:
        context.close()
