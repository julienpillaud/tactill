import httpx
import pytest

from tactill import TactillClient, TactillError
from tactill.entities.catalog.category import (
    Category,
    CategoryCreation,
    CategoryModification,
)


@pytest.mark.vcr()
def test_get_categories(client: TactillClient) -> None:
    limit = 30
    categories = client.get_categories(limit=limit)

    assert len(categories) == limit


@pytest.mark.vcr()
def test_get_categories_with_skip(client: TactillClient) -> None:
    categories = client.get_categories()
    categories_skip = client.get_categories(skip=1)

    assert categories_skip[0] == categories[1]


@pytest.mark.vcr()
def test_get_categories_with_filter(client: TactillClient) -> None:
    category_name = "BIÈRE"
    categories = client.get_categories(filter=f"name={category_name}")

    category = categories[0]
    assert category.name == category_name


@pytest.mark.vcr()
def test_get_categories_with_order(client: TactillClient) -> None:
    categories = client.get_categories(order="name=ASC")

    names = [category.name for category in categories if category.name]
    sorted_names = sorted(names)
    assert names == sorted_names


@pytest.mark.vcr()
def test_get_categories_bad_request(client: TactillClient) -> None:
    with pytest.raises(TactillError) as excinfo:
        client.get_categories(filter="bad")

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"


@pytest.mark.vcr()
def test_create_category(client: TactillClient) -> None:
    category_creation = CategoryCreation(
        test=False,
        color="#57DB47",
        icon_text="TEST",
        name="Test",
    )
    category = client.create_category(category_creation=category_creation)

    assert category.test == category_creation.test
    assert category.color == category_creation.color
    assert category.icon_text == category_creation.icon_text
    assert category.name == category_creation.name

    client.delete_category(category.id)


@pytest.mark.vcr()
def test_create_category_bad_request(client: TactillClient) -> None:
    category_creation = CategoryCreation(name="")
    with pytest.raises(TactillError) as excinfo:
        client.create_category(category_creation=category_creation)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
    assert (
        error.message
        == 'child "name" fails because ["name" is not allowed to be empty]'
    )


@pytest.mark.vcr()
def test_get_category(client: TactillClient) -> None:
    category_id = "5d83c74690924d0008f55d3a"
    category = client.get_category(category_id=category_id)

    assert category.id == category_id


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
def test_update_category(client: TactillClient, category: Category) -> None:
    category_modification = CategoryModification(name="NEW NAME")

    response = client.update_category(
        category_id=category.id, category_modification=category_modification
    )

    assert response.status_code == httpx.codes.OK
    assert response.message == "category successfully updated"

    updated_category = client.get_category(category_id=category.id)

    assert updated_category.version == category.version
    assert updated_category.deprecated == category.deprecated
    assert updated_category.created_at == category.created_at
    assert updated_category.updated_at != category.updated_at
    assert updated_category.original_id == category.original_id

    assert updated_category.company_id == category.company_id
    assert updated_category.is_default == category.is_default

    assert updated_category.test == category.test
    assert updated_category.image == category.image
    assert updated_category.color == category.color
    assert updated_category.icon_text == category.icon_text
    assert updated_category.name == category_modification.name


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
