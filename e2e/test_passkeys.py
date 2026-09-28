import json

import pytest
from playwright.sync_api import expect

from e2e.authenticators import PLATFORM, SECURITY_KEY

pytestmark = pytest.mark.integration


@pytest.mark.parametrize("authenticator", [PLATFORM, SECURITY_KEY])
def test_client_signs_up_and_in_with_a_passkey(new_site, authenticator):
    alice = new_site(authenticator)

    alice.sign_up_with_passkey("alice")
    expect(alice.page.locator("h2 b")).to_have_text("alice")
    alice.log_out()
    alice.log_in_with_passkey("alice")

    expect(alice.page.locator("h2 b")).to_have_text("alice")


def test_a_security_key_signs_in_from_another_computer(new_site):
    home = new_site(SECURITY_KEY)
    home.sign_up_with_passkey("alice")
    key_contents = home.authenticator.credentials()
    home.leave()

    work = new_site(SECURITY_KEY)
    for credential in key_contents:
        work.authenticator.add_credential(credential)
    work.log_in_with_passkey("alice")

    expect(work.page.locator("h2 b")).to_have_text("alice")


def test_an_authenticator_that_was_not_registered_cannot_sign_in(new_site):
    alice = new_site()
    alice.sign_up_with_passkey("alice")
    alice.leave()

    mallory = new_site()
    mallory.log_in_with_passkey("alice")

    expect(mallory.message()).to_contain_text("Could not sign in")
    assert not mallory.is_signed_in()


def test_a_captured_sign_in_cannot_be_replayed(new_site):
    alice = new_site()
    alice.sign_up_with_passkey("alice")
    alice.log_out()
    with alice.page.expect_request("**/passkeys/authentication") as sign_in:
        alice.log_in_with_passkey("alice")
    expect(alice.page.locator("h2 b")).to_have_text("alice")
    captured = sign_in.value.post_data
    alice.log_out()

    status = alice.page.evaluate(
        """body => fetch("/passkeys/authentication", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: body,
        }).then(response => response.status)""",
        captured
    )

    assert status == 401
    alice.page.goto(alice.web_app.url("/"))
    assert not alice.is_signed_in()
    assert json.loads(captured)["ceremony"]
