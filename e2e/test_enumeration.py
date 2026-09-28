import pytest

pytestmark = pytest.mark.integration

START_SIGN_IN = """login => fetch("/passkeys/authentication/options", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "X-CSRF-Token":
            document.querySelector('meta[name="csrf-token"]').content,
    },
    body: JSON.stringify({login}),
}).then(async response => ({
    status: response.status,
    body: await response.json(),
}))"""


def start_sign_in(site, login: str) -> dict:
    return site.page.evaluate(START_SIGN_IN, login)


def allowed_ids(answer: dict) -> list:
    return [credential["id"]
            for credential in answer["body"]["publicKey"]["allowCredentials"]]


def test_starting_to_sign_in_does_not_tell_whether_a_login_exists(new_site):
    alice = new_site()
    alice.sign_up_with_passkey("alice")
    alice.log_out()

    known = start_sign_in(alice, "alice")
    unknown = start_sign_in(alice, "nobody")
    unknown_again = start_sign_in(alice, "nobody")

    assert known["status"] == unknown["status"] == 200
    assert len(allowed_ids(known)) == len(allowed_ids(unknown)) == 1
    # A made-up answer would give itself away by changing every time.
    assert allowed_ids(unknown) == allowed_ids(unknown_again)


def test_ceremonies_cannot_be_started_without_limit(new_site):
    visitor = new_site()
    visitor.page.goto(visitor.web_app.url("/"))

    statuses = [start_sign_in(visitor, f"guess{n}")["status"]
                for n in range(30)]

    assert 429 in statuses
