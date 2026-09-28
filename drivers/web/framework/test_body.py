import pytest

from drivers.web.framework.body import Body, EmptyBody


def test_form_bodies_are_refined_into_fields():
    body = Body(b"login=alice&amount=10", "application/x-www-form-urlencoded")

    assert body.refine() == {"login": "alice", "amount": "10"}


@pytest.mark.parametrize("content_type", [
    "application/json",
    "application/json; charset=UTF-8",
    "Application/JSON",
])
def test_json_bodies_are_refined_into_values(content_type):
    body = Body('{"login": "alice", "n": [1, 2]}'.encode(), content_type)

    assert body.refine() == {"login": "alice", "n": [1, 2]}


def test_other_media_types_are_not_supported():
    with pytest.raises(NotImplementedError):
        Body(b"<x/>", "application/xml").refine()


def test_empty_body_refines_to_nothing():
    assert EmptyBody().refine() == b''
