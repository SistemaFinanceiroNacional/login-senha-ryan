import re

import pytest
from playwright.sync_api import Page, expect

from e2e.bank_site import BankSite


@pytest.mark.integration
def test_cents_add_up_exactly(page: Page, web_app):
    site = BankSite(page, web_app)
    site.sign_up_and_log_in("alice")
    site.open_account()

    for _ in range(3):
        site.deposit("0.10")

    expect(page.locator("section.account")).to_contain_text(
        re.compile(r"balance: 0\.30(?!\d)")
    )
