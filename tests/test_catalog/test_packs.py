import httpx
import pytest

from tactill.entities.pack import PackCreation
from tactill.tactill import ResponseError, TactillClient


def test_get_packs(client: TactillClient) -> None:
    limit = 1
    packs = client.get_packs(limit=limit)

    assert len(packs) == limit


def test_get_packs_with_skip(client: TactillClient) -> None:
    packs = client.get_packs()
    packs_skip = client.get_packs(skip=1)

    assert packs_skip[0] == packs[1]


def test_get_packs_with_filter(client: TactillClient) -> None:
    full_price = 1
    packs = client.get_packs(filter=f"full_price={full_price}")

    pack = packs[0]
    assert pack.full_price == full_price


def test_get_packs_with_order(client: TactillClient) -> None:
    packs = client.get_packs(order="full_price=ASC")

    prices = [pack.full_price for pack in packs if pack.full_price]
    sorted_prices = sorted(prices)
    assert prices == sorted_prices


def test_get_packs_bad_request(client: TactillClient) -> None:
    with pytest.raises(ResponseError) as excinfo:
        client.get_packs(filter="bad")

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"


def test_create_pack(client: TactillClient) -> None:
    pack_creation = PackCreation(
        articles=["5d85058251301a000790fc9b"],
        full_price=2,
        taxfree_price=1,
        taxes=[],
        discounts=[],
    )

    pack = client.create_pack(pack_creation=pack_creation)

    assert pack.articles[0] == pack_creation.articles[0]
    assert pack.taxes == pack_creation.taxes
    assert pack.discounts == pack_creation.discounts

    client.delete_pack(pack_id=pack.id)


def test_get_pack(client: TactillClient) -> None:
    pack_id = "64e5c46dde1d3600086b342f"
    pack = client.get_pack(pack_id=pack_id)

    assert pack.id == pack_id


def test_get_pack_not_found(client: TactillClient) -> None:
    pack_id = "14e5c46dde1d3600086b342f"

    with pytest.raises(ResponseError) as excinfo:
        client.get_pack(pack_id=pack_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.NOT_FOUND
    assert error.error == "Not Found"
    assert error.message == '"set_id" specified in "params" could not be found'


def test_get_pack_bad_request(client: TactillClient) -> None:
    pack_id = "1"

    with pytest.raises(ResponseError) as excinfo:
        client.get_pack(pack_id=pack_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
