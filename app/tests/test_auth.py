from app.core.auth import create_access_token, decode_access_token


def test_create_and_decode_access_token():
    token = create_access_token({"sub": "1"})

    assert token is not None
    assert isinstance(token, str)

    payload = decode_access_token(token)

    assert payload["sub"] == "1"