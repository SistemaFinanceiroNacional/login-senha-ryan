import pytest
from playwright.sync_api import expect

PAYLOAD = "<img src=x onerror=\"document.title='pwned'\">"


@pytest.mark.integration
def test_a_login_with_markup_is_shown_as_text(new_site):
    mallory = new_site()

    mallory.sign_up_with_passkey(PAYLOAD)

    expect(mallory.page.locator("h2 b")).to_have_text(PAYLOAD)
    assert mallory.page.title() != "pwned"
    assert mallory.page.locator("h2 b img").count() == 0
