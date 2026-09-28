from drivers.web.framework.httprequest.session import (
    expired_session_cookie,
    session_cookie
)


def attributes(cookie: str) -> list[str]:
    return [part.strip() for part in cookie.split(";")]


def test_session_cookie_is_sent_to_the_whole_site():
    assert "Path=/" in attributes(session_cookie("token"))
    assert "Path=/" in attributes(expired_session_cookie())


def test_the_session_cookie_only_carries_the_token():
    assert attributes(session_cookie("token"))[0] == "session=token"
