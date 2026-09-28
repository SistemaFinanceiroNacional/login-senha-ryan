import pytest

pytestmark = pytest.mark.integration


def test_pages_with_accents_arrive_whole(new_site):
    alice = new_site()
    alice.sign_up_with_passkey("alice")

    page = alice.page.evaluate(
        """() => fetch("/").then(response => response.text())"""
    )

    assert "Você está logado(a)!" in page
    assert page.rstrip().endswith("</html>")
