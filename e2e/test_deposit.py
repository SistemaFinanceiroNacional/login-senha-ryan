import pytest
from playwright.sync_api import Page, expect

from e2e.bank_site import BankSite


@pytest.mark.integration
def test_client_deposits_cash_and_sees_the_new_balance(page: Page, web_app):
    site = BankSite(page, web_app)
    site.sign_up_and_log_in("alice")
    site.open_account()
    expect(page.get_by_text("balance: 0")).to_be_visible()

    site.deposit("150.50")
    site.deposit("49.50")

    expect(page.get_by_text("balance: 200.0")).to_be_visible()
    expect(page.locator("ol li")).to_have_count(2)


@pytest.mark.integration
@pytest.mark.parametrize("amount", ["0", "-10", "nan", "inf", "abc"])
def test_invalid_amounts_are_rejected(page: Page, web_app, amount):
    site = BankSite(page, web_app)
    site.sign_up_and_log_in("alice")
    site.open_account()

    assert site.deposit_bypassing_form_validation(amount) == 400

    page.goto(web_app.url("/selectaccount"))
    expect(page.get_by_text("balance: 0")).to_be_visible()
