import pytest
from playwright.sync_api import Page, expect


@pytest.mark.integration
def test_visitor_registers_and_logs_in(page: Page, web_app):
    page.goto(web_app.url("/register"))
    page.fill("input[name=newUsername]", "alice")
    page.fill("input[name=newPassword]", "alicepw")
    page.click("input[type=submit]")

    page.fill("input[name=login]", "alice")
    page.fill("input[name=password]", "alicepw")
    page.click("input[type=submit]")

    expect(page.get_by_text("Você está logado(a)!")).to_be_visible()
    expect(page.locator("h2 b")).to_have_text("alice")
