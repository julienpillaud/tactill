import httpx
import pytest

from tactill import TactillClient, TactillError


def test_client(api_key: str) -> None:
    client = TactillClient(api_key=api_key)

    assert client.account
    assert client.company_id
    assert client.node_id
    assert client.shop_id


def test_client_api_key() -> None:
    with pytest.raises(TactillError) as excinfo:
        TactillClient(api_key="")

    assert excinfo.value.error.status_code == httpx.codes.UNAUTHORIZED
