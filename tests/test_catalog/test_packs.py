import httpx
import pytest

from tactill import FilterEntity, QueryParams, TactillClient, TactillError
from tactill.entities import Pack


@pytest.mark.vcr()
def test_get_packs(client: TactillClient) -> None:
    limit = 1
    query = QueryParams(limit=limit)
    packs = client.get_packs(query=query)

    assert len(packs) == limit


@pytest.mark.vcr()
def test_get_packs_with_skip(client: TactillClient) -> None:
    packs = client.get_packs()
    query = QueryParams(skip=1)
    packs_skip = client.get_packs(query=query)

    assert packs_skip[0] == packs[1]


@pytest.mark.vcr()
def test_get_packs_with_filter(client: TactillClient, pack: Pack) -> None:
    full_price = pack.full_price
    query = QueryParams(filters=[FilterEntity(field="full_price", value=full_price)])
    packs = client.get_packs(query=query)

    pack = packs[0]
    assert pack.full_price == full_price


@pytest.mark.vcr()
def test_get_packs_with_order(client: TactillClient) -> None:
    query = QueryParams(order="full_price=ASC")
    packs = client.get_packs(query=query)

    prices = [pack.full_price for pack in packs if pack.full_price]
    sorted_prices = sorted(prices)
    assert prices == sorted_prices


@pytest.mark.vcr()
def test_get_pack(client: TactillClient, pack: Pack) -> None:
    created_pack = client.get_pack(pack_id=pack.id)

    assert created_pack.id == pack.id


@pytest.mark.vcr()
def test_get_pack_not_found(client: TactillClient) -> None:
    pack_id = "14e5c46dde1d3600086b342f"

    with pytest.raises(TactillError) as excinfo:
        client.get_pack(pack_id=pack_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.NOT_FOUND
    assert error.error == "Not Found"
    assert error.message == '"set_id" specified in "params" could not be found'


@pytest.mark.vcr()
def test_get_pack_bad_request(client: TactillClient) -> None:
    pack_id = "1"

    with pytest.raises(TactillError) as excinfo:
        client.get_pack(pack_id=pack_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
