import pytest
from playwright.sync_api import Page, expect

from e2e.bank_site import BankSite


@pytest.mark.integration
def test_visitor_signs_up_and_is_signed_in(page: Page, web_app):
    site = BankSite(page, web_app)

    site.sign_up_with_passkey("alice")

    expect(page.get_by_text("Você está logado(a)!")).to_be_visible()
    expect(page.locator("h2 b")).to_have_text("alice")
