import pytest
from playwright.sync_api import expect

from e2e.bank_site import SIGNED_IN, BankSite

pytestmark = pytest.mark.integration


def cookie(name: str, value: str, site: BankSite) -> dict:
    return {"name": name, "value": value, "url": site.web_app.url("/")}


def test_a_forged_session_cookie_gives_no_access(new_site):
    alice = new_site()
    alice.sign_up_with_passkey("alice")
    alice.leave()

    mallory = new_site()
    mallory.page.context.add_cookies([
        cookie("loggedUsername", '{"client_id":1,"login":"alice"}', mallory),
        cookie("session", "a-guessed-token", mallory),
    ])
    mallory.page.goto(mallory.web_app.url("/"))

    assert not mallory.is_signed_in()


def test_a_session_ends_with_the_log_out(new_site):
    alice = new_site()
    alice.sign_up_with_passkey("alice")
    stolen = alice.page.context.cookies()

    alice.log_out()
    alice.page.context.add_cookies(stolen)
    alice.page.goto(alice.web_app.url("/"))

    assert not alice.is_signed_in()


def test_signing_in_starts_a_new_session(new_site):
    """An attacker who planted a session id in the victim's browser must
    not end up sharing the victim's signed-in session (fixation)."""
    alice = new_site()
    alice.sign_up_with_passkey("alice")
    alice.log_out()
    alice.page.context.add_cookies([cookie("session", "planted", alice)])

    alice.log_in_with_passkey("alice")

    expect(alice.page.get_by_text(SIGNED_IN)).to_be_visible()
    [session] = [c for c in alice.page.context.cookies()
                 if c["name"] == "session"]
    assert session["value"] != "planted"


def test_scripts_cannot_read_the_session_cookie(new_site):
    alice = new_site()
    alice.sign_up_with_passkey("alice")

    readable = alice.page.evaluate("document.cookie")

    assert "session=" not in readable
