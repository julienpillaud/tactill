from datetime import datetime

import httpx
import pytest

from tactill import TactillClient, TactillError
from tactill.entities.catalog.discount import (
    Discount,
    DiscountCreation,
    DiscountModification,
)


@pytest.mark.vcr()
def test_get_discounts(client: TactillClient) -> None:
    limit = 10
    discounts = client.get_discounts(limit=limit)

    assert len(discounts) == limit


@pytest.mark.vcr()
def test_get_discounts_with_skip(client: TactillClient) -> None:
    discounts = client.get_discounts()
    discounts_skip = client.get_discounts(skip=1)

    assert discounts_skip[0] == discounts[1]


@pytest.mark.vcr()
def test_get_discounts_with_filter(client: TactillClient) -> None:
    discount_name = "Offert"
    discounts = client.get_discounts(filter=f"name={discount_name}")

    discount = discounts[0]
    assert discount.name == discount_name


@pytest.mark.vcr()
def test_get_discounts_with_order(client: TactillClient) -> None:
    discounts = client.get_discounts(order="name=ASC")

    names = [discount.name for discount in discounts if discount.name]
    sorted_names = sorted(names)
    assert names == sorted_names


@pytest.mark.vcr()
def test_get_discounts_bad_request(client: TactillClient) -> None:
    with pytest.raises(TactillError) as excinfo:
        client.get_discounts(filter="bad")

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"


@pytest.mark.vcr()
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


@pytest.mark.vcr()
def test_get_discount(client: TactillClient) -> None:
    discount_id = "5d70d4e6be8f9f001195cccb"
    discount = client.get_discount(discount_id=discount_id)

    assert discount.id == discount_id


@pytest.mark.vcr()
def test_get_discount_not_found(client: TactillClient) -> None:
    discount_id = "1d70d4e6be8f9f001195cccb"

    with pytest.raises(TactillError) as excinfo:
        client.get_discount(discount_id=discount_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.NOT_FOUND
    assert error.error == "Not Found"
    assert error.message == '"discount_id" specified in "params" could not be found'


@pytest.mark.vcr()
def test_get_discount_bad_request(client: TactillClient) -> None:
    discount_id = "1"

    with pytest.raises(TactillError) as excinfo:
        client.get_discount(discount_id=discount_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"


@pytest.mark.vcr()
def test_update_discount(client: TactillClient, discount: Discount) -> None:
    discount_modification = DiscountModification(name="NEW NAME")

    response = client.update_discount(
        discount_id=discount.id, discount_modification=discount_modification
    )

    assert response.status_code == httpx.codes.OK
    assert response.message == "discount successfully updated"

    updated_discount = client.get_discount(discount_id=discount.id)

    assert updated_discount.version == discount.version
    assert updated_discount.deprecated == discount.deprecated
    assert updated_discount.created_at == discount.created_at
    assert updated_discount.updated_at != discount.updated_at
    assert updated_discount.original_id == discount.original_id

    assert updated_discount.shop_id == discount.shop_id

    assert updated_discount.test == discount.test
    assert updated_discount.name == discount_modification.name
    assert updated_discount.rate == discount.rate
    assert updated_discount.type == discount.type
    assert updated_discount.start_date == discount.start_date
    assert updated_discount.end_date == discount.end_date
    assert updated_discount.barcode == discount.barcode
    assert updated_discount.icon_text == discount.icon_text
    assert updated_discount.color == discount.color


@pytest.mark.vcr()
def test_update_discount_bad_request(client: TactillClient, discount: Discount) -> None:
    discount_modification = DiscountModification(name="")

    with pytest.raises(TactillError) as excinfo:
        client.update_discount(
            discount_id=discount.id, discount_modification=discount_modification
        )

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
