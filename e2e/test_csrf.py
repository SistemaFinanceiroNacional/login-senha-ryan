import pytest
from playwright.sync_api import expect

from e2e.bank_site import SIGNED_IN

NO_CSRF_PROTECTION = "requests are not protected against CSRF (issue #101)"

pytestmark = [
    pytest.mark.integration,
    pytest.mark.xfail(strict=True, reason=NO_CSRF_PROTECTION,
                      raises=AssertionError),
]


def test_a_form_without_the_anti_csrf_token_is_refused(new_site):
    alice = new_site()
    alice.sign_up_with_passkey("alice")
    alice.open_account()

    status = alice.submit_hand_made_form("/deposit", {"amount": "100"})

    assert status == 403
    alice.page.goto(alice.web_app.url("/selectaccount"))
    expect(alice.page.get_by_text("balance: 0.00")).to_be_visible()


def test_a_json_request_without_the_anti_csrf_token_is_refused(new_site):
    visitor = new_site()
    visitor.page.goto(visitor.web_app.url("/register"))

    status = visitor.page.evaluate(
        """() => fetch("/passkeys/registration/options", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({login: "alice"}),
        }).then(response => response.status)"""
    )

    assert status == 403


def test_another_site_cannot_log_the_client_out(new_site):
    alice = new_site()
    alice.sign_up_with_passkey("alice")
    bank = alice.web_app.base_url

    # A page on another site (127.0.0.1 is not the same site as
    # localhost) posts a form to the bank.
    alice.page.goto(bank.replace("localhost", "127.0.0.1") + "/register")
    alice.submit_hand_made_form(bank + "/logout", {})
    alice.page.wait_for_url(bank + "/")

    expect(alice.page.get_by_text(SIGNED_IN)).to_be_visible()
