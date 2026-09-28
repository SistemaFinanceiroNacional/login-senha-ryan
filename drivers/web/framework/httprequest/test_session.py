import pytest

from drivers.web.framework.httprequest.session import Session


@pytest.mark.xfail(strict=True, raises=AssertionError,
                   reason="session cookie has no Path (issue #102)")
def test_session_cookie_is_sent_to_the_whole_site():
    cookie = Session({"login": "alice"}).to_headers()["Set-Cookie"]

    attributes = [part.strip() for part in cookie.split(";")]
    assert "Path=/" in attributes
