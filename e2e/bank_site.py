from playwright.sync_api import Page, expect

from e2e.authenticators import PLATFORM, VirtualAuthenticator

SIGNED_IN = "Você está logado(a)!"


class BankSite:
    """What a client can do on the web application, expressed as user
    actions on the pages."""

    def __init__(self, page: Page, web_app, authenticator: str = PLATFORM):
        self.page = page
        self.web_app = web_app
        self.authenticator = VirtualAuthenticator(page, authenticator)

    def sign_up_and_log_in(self, login: str) -> None:
        """Signing up with a passkey leaves the new client signed in."""
        self.sign_up_with_passkey(login)

    def sign_up_with_passkey(self, login: str) -> None:
        self.page.goto(self.web_app.url("/register"))
        self.page.fill("form#sign-up input[name=login]", login)
        self.page.click("form#sign-up [type=submit]")
        expect(self.page.get_by_text(SIGNED_IN)).to_be_visible()

    def log_in_with_passkey(self, login: str) -> None:
        self.page.goto(self.web_app.url("/"))
        self.page.fill("form#sign-in input[name=login]", login)
        self.page.click("form#sign-in [type=submit]")

    def is_signed_in(self) -> bool:
        return self.page.get_by_text(SIGNED_IN).is_visible()

    def log_out(self) -> None:
        self.page.click("form[action='/logout'] [type=submit]")

    def submit_hand_made_form(self, action: str, fields: dict) -> int:
        """Posts a form built in the browser (as anyone can do from the
        developer tools or from another page) and returns the status."""
        with self.page.expect_response(
            lambda response: response.request.method == "POST"
        ) as answer:
            self.page.evaluate(
                """([action, fields]) => {
                    const form = document.createElement("form");
                    form.method = "post";
                    form.action = action;
                    for (const [name, value] of Object.entries(fields)) {
                        const input = document.createElement("input");
                        input.name = name;
                        input.value = value;
                        form.appendChild(input);
                    }
                    document.body.appendChild(form);
                    form.submit();
                }""",
                [action, fields]
            )
        return answer.value.status

    def message(self):
        return self.page.locator("#message")

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
