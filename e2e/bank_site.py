from playwright.sync_api import Page

PASSWORD = "secret"


class BankSite:
    """What a client can do on the web application, expressed as user
    actions on the pages."""

    def __init__(self, page: Page, web_app):
        self.page = page
        self.web_app = web_app

    def sign_up(self, login: str) -> None:
        self.page.goto(self.web_app.url("/register"))
        self.page.fill("input[name=newUsername]", login)
        self.page.fill("input[name=newPassword]", PASSWORD)
        self.page.click("input[type=submit]")

    def log_in(self, login: str) -> None:
        self.page.goto(self.web_app.url("/"))
        self.page.fill("input[name=login]", login)
        self.page.fill("input[name=password]", PASSWORD)
        self.page.click("input[type=submit]")

    def sign_up_and_log_in(self, login: str) -> None:
        self.sign_up(login)
        self.log_in(login)

    def account_ids(self) -> list[int]:
        buttons = self.page.locator("form[action='/selectaccount'] button")
        values = buttons.evaluate_all("buttons => buttons.map(b => b.value)")
        return [int(value) for value in values]

    def open_account(self) -> None:
        self.page.click("form[action='/selectaccount'] button")

    def leave(self) -> None:
        self.page.context.close()

    def deposit(self, amount: str) -> None:
        self.page.fill("input[name=amount]", amount)
        self.page.click("form[action='/deposit'] input[type=submit]")

    def deposit_bypassing_form_validation(self, amount: str) -> int:
        """Turns the amount field into free text, as anyone can do in the
        browser, submits it and returns the response status."""
        field = "input[name=amount]"
        self.page.eval_on_selector(
            field, "input => { input.type = 'text'; input.required = false; }"
        )
        self.page.fill(field, amount)
        with self.page.expect_response(
            lambda response: response.request.method == "POST"
        ) as deposit:
            self.page.click("form[action='/deposit'] input[type=submit]")
        return deposit.value.status
