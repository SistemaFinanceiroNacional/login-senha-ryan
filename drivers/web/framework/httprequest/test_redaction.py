from drivers.web.framework.httprequest.http_request import redacted


def test_headers_granting_access_are_redacted():
    headers = {"Host": "bank", "Cookie": "session=secret",
               "X-CSRF-Token": "token", "authorization": "Bearer x"}

    assert redacted(headers) == {
        "Host": "bank", "Cookie": "<redacted>",
        "X-CSRF-Token": "<redacted>", "authorization": "<redacted>",
    }
