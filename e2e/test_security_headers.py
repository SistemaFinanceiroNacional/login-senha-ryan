import pytest

pytestmark = pytest.mark.integration


def assert_protected(response) -> None:
    headers = response.headers
    policy = headers.get("content-security-policy", "")
    assert "default-src 'self'" in policy
    assert "script-src 'self'" in policy
    assert "frame-ancestors 'none'" in policy
    assert headers.get("x-frame-options") == "DENY"
    assert headers.get("x-content-type-options") == "nosniff"
    assert headers.get("referrer-policy") == "same-origin"
    assert "no-store" in headers.get("cache-control", "")


def test_pages_are_served_with_security_headers(new_site):
    alice = new_site()
    assert_protected(alice.page.goto(alice.web_app.url("/")))
    assert_protected(alice.page.goto(alice.web_app.url("/register")))

    alice.sign_up_with_passkey("alice")
    assert_protected(alice.page.goto(alice.web_app.url("/")))
    alice.open_account()
    assert_protected(alice.page.goto(alice.web_app.url("/selectaccount")))


def test_pages_work_within_their_content_security_policy(new_site):
    alice = new_site()
    violations = []
    alice.page.on("console", lambda message: violations.append(message.text)
                  if "Content Security Policy" in message.text else None)

    alice.sign_up_with_passkey("alice")
    alice.log_out()
    alice.log_in_with_passkey("alice")
    alice.open_account()
    alice.deposit("10")

    assert violations == []
