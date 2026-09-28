import pytest

from drivers.web.framework.encodings import url_encoded
from drivers.web.framework.httprequest.http_request import HttpRequest
from drivers.web.framework.httprequest.resource import make_resource
from drivers.web.framework.staticfiles import StaticFiles


@pytest.fixture
def static(tmp_path):
    (tmp_path / "site.css").write_text("body{}")
    (tmp_path / "secret.txt").write_text("secret")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "inner.css").write_text("p{}")
    return StaticFiles(tmp_path, "/static/")


def get(files, path, method="GET"):
    return files(HttpRequest({}, b"", method,
                             make_resource(path, url_encoded), "1.1"))


def test_a_file_is_served_with_its_type(static):
    response = get(static, "/static/site.css")

    assert response.get_status() == 200
    assert response.get_body() == b"body{}"
    assert response.get_headers()["Content-Type"].startswith("text/css")


@pytest.mark.parametrize("path", [
    "/static/missing.css",
    "/static/secret.txt",
    "/static/../static/site.css",
    "/static/sub/inner.css",
    "/static/.hidden.css",
    "/static/",
])
def test_anything_else_is_not_found(static, path):
    assert get(static, path).get_status() == 404


def test_files_cannot_be_changed(static):
    assert get(static, "/static/site.css", "POST").get_status() == 405
