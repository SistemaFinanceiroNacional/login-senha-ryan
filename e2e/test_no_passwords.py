import pytest

pytestmark = [
    pytest.mark.integration,
    pytest.mark.xfail(strict=True, raises=AssertionError,
                      reason="the web still accepts passwords (issue #119)"),
]


def submit_form(site, action: str, fields: dict) -> int:
    """Posts a hand-made form from the browser, returning the status."""
    with site.page.expect_response(
        lambda response: response.request.method == "POST"
    ) as answer:
        site.page.evaluate(
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


@pytest.mark.parametrize("action, fields", [
    ("/register", {"newUsername": "alice", "newPassword": "secret"}),
    ("/", {"login": "alice", "password": "secret"}),
])
def test_passwords_are_not_accepted(new_site, action, fields):
    visitor = new_site()
    visitor.page.goto(visitor.web_app.url("/"))

    assert submit_form(visitor, action, fields) == 405
