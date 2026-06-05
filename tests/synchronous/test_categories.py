import httpx
import pytest

from tactill import (
    Category,
    CategoryUpdate,
    TactillClient,
    TactillColor,
    TactillUUID,
)
from tactill.data import CATEGORIES


@pytest.mark.skip_on_ci
def test_get_categories(client: TactillClient) -> None:
    results = client.categories.get_all()

    assert len(results) == len(CATEGORIES)
    for result in results:
        assert result.deprecated is False
        assert result.name in CATEGORIES


@pytest.mark.skip_on_ci
def test_get_category(client: TactillClient) -> None:
    results = client.categories.get_all(limit=1)
    category = results[0]

    response = client.categories.get(category_id=category.id)

    assert response.id == category.id
    assert response.deprecated == category.deprecated
    assert response.name == category.name
    assert response.color == category.color
    assert response.icon_text == category.icon_text


@pytest.mark.skip_on_ci
def test_update_category(client: TactillClient, category_id: TactillUUID) -> None:
    category = client.categories.get(category_id=category_id)
    category_update = build_category_update(
        category,
        name=True,
        color=True,
        icon_text=True,
    )

    response = client.categories.update(
        category_id=category.id,
        data=category_update,
    )

    assert response.status_code == httpx.codes.OK
    assert response.error == ""
    assert response.message == "category successfully updated"

    updated_category = client.categories.get(category_id=category.id)

    assert updated_category.id == category.id
    assert updated_category.deprecated == category.deprecated
    assert updated_category.name == category_update.name
    assert updated_category.color == category_update.color
    assert updated_category.icon_text == category_update.icon_text


def build_category_update(
    category: Category,
    /,
    name: bool,
    color: bool,
    icon_text: bool,
) -> CategoryUpdate:
    category_name = None
    if name:
        name_split, number_split = category.name.split(" - ")
        category_name = f"{name_split} - {int(number_split) + 1}"

    category_color = category.color
    if color:
        category_color = (
            TactillColor.MAGENTA
            if category.color == TactillColor.PURPLE
            else TactillColor.PURPLE
        )

    category_icon_text = None
    if icon_text:
        category_icon_text = (
            category.icon_text.lower()
            if category.icon_text.isupper()
            else category.icon_text.upper()
        )

    return CategoryUpdate(
        name=category_name,
        color=category_color,
        icon_text=category_icon_text,
    )
