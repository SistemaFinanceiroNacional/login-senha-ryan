import pytest

pytestmark = pytest.mark.integration


@pytest.mark.parametrize("action, fields", [
    ("/register", {"newUsername": "alice", "newPassword": "secret"}),
    ("/", {"login": "alice", "password": "secret"}),
])
def test_passwords_are_not_accepted(new_site, action, fields):
    visitor = new_site()
    visitor.page.goto(visitor.web_app.url("/"))

    assert visitor.submit_hand_made_form(action, fields) == 405
