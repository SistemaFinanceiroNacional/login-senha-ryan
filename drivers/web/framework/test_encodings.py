from drivers.web.framework.encodings import url_encoded


def test_fields_are_decoded():
    assert url_encoded("login=ana%20maria&amount=10.50") == \
        {"login": "ana maria", "amount": "10.50"}


def test_fields_without_value_are_empty():
    assert url_encoded("debug") == {"debug": ""}
    assert url_encoded("") == {}
