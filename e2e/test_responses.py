import pytest

pytestmark = pytest.mark.integration


@pytest.mark.xfail(strict=True, raises=AssertionError,
                   reason="Content-length counts characters (issue #122)")
def test_pages_with_accents_arrive_whole(new_site):
    alice = new_site()
    alice.sign_up_with_passkey("alice")

    page = alice.page.evaluate(
        """() => fetch("/").then(response => response.text())"""
    )

    assert "Você está logado(a)!" in page
    assert page.rstrip().endswith("</html>")
