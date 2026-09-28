import pytest

pytestmark = pytest.mark.integration


def test_secrets_are_never_logged(new_site):
    alice = new_site()
    alice.sign_up_with_passkey("alice")
    alice.open_account()
    alice.deposit("10")

    [session] = [c["value"] for c in alice.page.context.cookies()
                 if c["name"] == "session"]
    csrf_token = alice.csrf_token()
    logs = alice.web_app.logs()

    assert "Resource:" in logs, "the application does log requests"
    assert session not in logs
    assert csrf_token not in logs
    assert "attestationObject" not in logs
