from tactill import TactillClient


def test_client(api_key: str) -> None:
    client = TactillClient(api_key=api_key)

    assert client.account
    assert client.company_id
    assert client.node_id
    assert client.shop_id
