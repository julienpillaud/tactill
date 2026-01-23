import httpx
import pytest

from tactill import QueryParams, TactillClient, TactillColor, TactillError
from tactill.entities.catalog.category import (
    Category,
    CategoryCreation,
    CategoryModification,
)
from tactill.filters import FilterEntity


@pytest.mark.vcr()
def test_get_categories(client: TactillClient) -> None:
    limit = 30
    query = QueryParams(limit=limit)
    categories = client.get_categories(query=query)

    assert len(categories) == limit


@pytest.mark.vcr()
def test_get_categories_with_skip(client: TactillClient) -> None:
    categories = client.get_categories()
    query = QueryParams(skip=1)
    categories_skip = client.get_categories(query=query)

    assert categories_skip[0] == categories[1]


@pytest.mark.vcr()
def test_get_categories_with_filter(client: TactillClient) -> None:
    category_name = "BIÈRE"
    query = QueryParams(filters=[FilterEntity(field="name", value=category_name)])
    categories = client.get_categories(query=query)

    category = categories[0]
    assert category.name == category_name


@pytest.mark.vcr()
def test_get_categories_with_order(client: TactillClient) -> None:
    query = QueryParams(order="name=ASC")
    categories = client.get_categories(query=query)

    names = [category.name for category in categories if category.name]
    sorted_names = sorted(names)
    assert names == sorted_names


@pytest.mark.vcr()
def test_create_category(client: TactillClient) -> None:
    category_creation = CategoryCreation(
        test=False,
        color=TactillColor.GREEN,
        icon_text="TEST",
        name="Test",
    )
    category = client.create_category(category_creation=category_creation)

    assert category.test == category_creation.test
    assert category.color == category_creation.color
    assert category.icon_text == category_creation.icon_text
    assert category.name == category_creation.name

    response = client.delete_category(category.id)
    # Ensure category is deleted
    assert response.status_code == httpx.codes.OK


@pytest.mark.vcr()
def test_create_category_bad_request(client: TactillClient) -> None:
    category_creation = CategoryCreation(name="")
    with pytest.raises(TactillError) as excinfo:
        client.create_category(category_creation=category_creation)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
    assert error.message == "Invalid request payload input"


@pytest.mark.vcr()
def test_get_category(client: TactillClient, category: Category) -> None:
    created_category = client.get_category(category_id=category.id)

    assert created_category.id == category.id


@pytest.mark.vcr()
def test_get_category_not_found(client: TactillClient) -> None:
    category_id = "1d83c74690924d0008f55d3a"

    with pytest.raises(TactillError) as excinfo:
        client.get_category(category_id=category_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.NOT_FOUND
    assert error.error == "Not Found"
    assert error.message == '"category_id" specified in "params" could not be found'


@pytest.mark.vcr()
def test_get_category_bad_request(client: TactillClient) -> None:
    category_id = "1"

    with pytest.raises(TactillError) as excinfo:
        client.get_category(category_id=category_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"


@pytest.mark.vcr()
def test_update_category_bad_request(client: TactillClient, category: Category) -> None:
    category_modification = CategoryModification(name="")

    with pytest.raises(TactillError) as excinfo:
        client.update_category(
            category_id=category.id, category_modification=category_modification
        )

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
