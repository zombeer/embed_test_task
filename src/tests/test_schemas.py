import pytest
from pydantic import ValidationError
from schemas.inbound import NewPostPayload


def test_new_post_payload():
    payload = dict(
        title="normal_title",
        text="normal_text",
    )
    assert NewPostPayload(**payload), "Must return a valid post"

    with pytest.raises(ValidationError):
        payload = dict(
            title="long_title" * 10,
            text="normal_text",
        )
        assert NewPostPayload(
            **payload
        ), "Must raise validation error because of too long title"

    with pytest.raises(ValidationError):
        payload = dict(
            title="normal_title",
            text="super_long_text" * 1000,
        )
        assert NewPostPayload(
            **payload
        ), "Must raise validation error because of too long text"
