import importlib

import pytest

from drivers.web.framework import settings
from drivers.web.framework.template import render_template

AUTOESCAPE_OFF = "Jinja2 renders templates without autoescape (issue #100)"
SCRIPT = "<script>alert('xss')</script>"


@pytest.fixture(autouse=True)
def application_templates():
    # The same way the framework loads the application's settings.
    settings.app_settings = importlib.import_module(
        "drivers.web.application.settings"
    )


@pytest.mark.xfail(strict=True, reason=AUTOESCAPE_OFF, raises=AssertionError)
def test_user_data_is_rendered_as_text_not_markup():
    page = render_template("loggedPage.html", {"user": SCRIPT, "accounts": []})

    assert SCRIPT not in page
    assert "&lt;script&gt;alert(&#39;xss&#39;)&lt;/script&gt;" in page


@pytest.mark.xfail(strict=True, reason=AUTOESCAPE_OFF, raises=AssertionError)
def test_user_data_cannot_break_out_of_attributes():
    page = render_template(
        "loggedPage.html", {"user": "alice", "accounts": ['1" autofocus x="']}
    )

    assert 'value="1" autofocus' not in page
