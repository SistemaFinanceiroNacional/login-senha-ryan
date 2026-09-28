import pytest
from playwright.sync_api import expect

from e2e.bank_site import BankSite

BOB_BALANCE = "500.00"


@pytest.fixture
def alice(new_site) -> BankSite:
    alice = new_site()
    alice.sign_up_and_log_in("alice")
    return alice


@pytest.fixture
def bob_account(new_site) -> int:
    bob = new_site()
    bob.sign_up_and_log_in("bob")
    [account] = bob.account_ids()
    bob.open_account()
    bob.deposit("500")
    expect(bob.page.get_by_text(f"balance: {BOB_BALANCE}")).to_be_visible()
    bob.leave()
    return account


@pytest.mark.integration
def test_client_opens_own_account(alice):
    alice.open_account()
    alice.deposit("100")

    expect(alice.page.get_by_text("balance: 100.00")).to_be_visible()


@pytest.mark.integration
def test_anonymous_visitor_cannot_open_an_account(new_site, bob_account):
    visitor = new_site()
    visitor.page.goto(visitor.web_app.url("/"))

    # Without logging in, the visitor submits a hand-made form.
    with visitor.page.expect_navigation():
        visitor.page.evaluate(
            """accountId => {
                const form = document.createElement("form");
                form.method = "post";
                form.action = "/selectaccount";
                const field = document.createElement("input");
                field.name = "account_id";
                field.value = accountId;
                form.appendChild(field);
                document.body.appendChild(form);
                form.submit();
            }""",
            str(bob_account)
        )
    visitor.page.goto(visitor.web_app.url("/selectaccount"))

    assert BOB_BALANCE not in visitor.page.content()


@pytest.mark.integration
def test_client_cannot_open_another_clients_account(bob_account, alice):
    # Alice edits her account button in the browser to point to Bob's.
    alice.page.eval_on_selector(
        "form[action='/selectaccount'] button",
        "(button, accountId) => button.value = accountId",
        str(bob_account)
    )

    with alice.page.expect_response(
        lambda response: response.request.method == "POST"
    ) as selection:
        alice.open_account()

    assert selection.value.status == 404
    assert BOB_BALANCE not in alice.page.content()


@pytest.mark.integration
def test_non_numeric_account_is_not_found(alice):
    alice.page.eval_on_selector(
        "form[action='/selectaccount'] button",
        "button => button.value = 'abc'"
    )

    with alice.page.expect_response(
        lambda response: response.request.method == "POST"
    ) as selection:
        alice.open_account()

    assert selection.value.status == 404
