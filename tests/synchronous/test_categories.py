import pytest

from tactill import (
    FilterEntity,
    FilterOperator,
    TactillClient,
)
from tests.data import CATEGORIES


@pytest.mark.skip_on_ci
def test_get_categories(client: TactillClient) -> None:
    results = client.categories.get_all(
        filters=[
            FilterEntity(field="name", value=CATEGORIES, operator=FilterOperator.IN)
        ]
    )

    assert len(results) == len(CATEGORIES)
    for result in results:
        assert result.deprecated is False
        assert result.name in CATEGORIES


@pytest.mark.skip_on_ci
def test_get_category(client: TactillClient) -> None:
    results = client.categories.get_all(
        limit=1,
        filters=[
            FilterEntity(field="name", value=CATEGORIES, operator=FilterOperator.IN)
        ],
    )
    category = results[0]

    response = client.categories.get(category_id=category.id)

    assert response.id == category.id
    assert response.deprecated == category.deprecated
    assert response.name == category.name
    assert response.color == category.color
    assert response.icon_text == category.icon_text
