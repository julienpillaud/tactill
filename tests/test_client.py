import pytest

from tactill.tactill import TactillClient


def test_connexion(api_key: str) -> None:
    client = TactillClient(api_key=api_key)

    assert client.account


def test_bad_connexion() -> None:
    with pytest.raises(ConnectionError):
        TactillClient(api_key="")
