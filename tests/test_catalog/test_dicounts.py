from datetime import datetime

import httpx
import pytest

from tactill.entities.discount import DiscountCreation
from tactill.tactill import ResponseError, TactillClient


def test_get_discounts(client: TactillClient) -> None:
    limit = 10
    discounts = client.get_discounts(limit=limit)

    assert len(discounts) == limit


def test_get_discounts_with_skip(client: TactillClient) -> None:
    discounts = client.get_discounts()
    discounts_skip = client.get_discounts(skip=1)

    assert discounts_skip[0] == discounts[1]


def test_get_discounts_with_filter(client: TactillClient) -> None:
    discount_name = "Offert"
    discounts = client.get_discounts(filter=f"name={discount_name}")

    discount = discounts[0]
    assert discount.name == discount_name


def test_get_discounts_with_order(client: TactillClient) -> None:
    discounts = client.get_discounts(order="name=ASC")

    names = [discount.name for discount in discounts if discount.name]
    sorted_names = sorted(names)
    assert names == sorted_names


def test_get_discounts_bad_request(client: TactillClient) -> None:
    with pytest.raises(ResponseError) as excinfo:
        client.get_discounts(filter="bad")

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"


def test_create_discount(client: TactillClient) -> None:
    discount_creation = DiscountCreation(
        test=False,
        name="Test",
        rate=1,
        type="rate",
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 12, 31),
        barcode="123",
        icon_text="TEST",
        color="#57DB47",
    )
    discount = client.create_discount(discount_creation=discount_creation)

    assert discount.test == discount_creation.test
    assert discount.name == discount_creation.name
    assert discount.rate == discount_creation.rate
    assert discount.type == discount_creation.type
    assert discount.start_date
    assert discount.start_date.replace(tzinfo=None) == discount_creation.start_date
    assert discount.end_date
    assert discount.end_date.replace(tzinfo=None) == discount_creation.end_date
    assert discount.barcode == discount_creation.barcode
    assert discount.icon_text == discount_creation.icon_text
    assert discount.color == discount_creation.color

    client.delete_discount(discount.id)


def test_get_discount(client: TactillClient) -> None:
    discount_id = "5d70d4e6be8f9f001195cccb"
    discount = client.get_discount(discount_id=discount_id)

    assert discount.id == discount_id


def test_get_discount_not_found(client: TactillClient) -> None:
    discount_id = "1d70d4e6be8f9f001195cccb"

    with pytest.raises(ResponseError) as excinfo:
        client.get_discount(discount_id=discount_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.NOT_FOUND
    assert error.error == "Not Found"
    assert error.message == '"discount_id" specified in "params" could not be found'


def test_get_discount_bad_request(client: TactillClient) -> None:
    discount_id = "1"

    with pytest.raises(ResponseError) as excinfo:
        client.get_discount(discount_id=discount_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
