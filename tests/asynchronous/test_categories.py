import pytest

from tactill import (
    AsyncTactillClient,
    FilterEntity,
    FilterOperator,
)
from tests.data import CATEGORIES


@pytest.mark.skip_on_ci
@pytest.mark.anyio
async def test_get_categories(aclient: AsyncTactillClient) -> None:
    results = await aclient.categories.get_all(
        filters=[
            FilterEntity(field="name", value=CATEGORIES, operator=FilterOperator.IN)
        ]
    )

    assert len(results) == len(CATEGORIES)
    for result in results:
        assert result.deprecated is False
        assert result.name in CATEGORIES


@pytest.mark.skip_on_ci
@pytest.mark.anyio
async def test_get_category(aclient: AsyncTactillClient) -> None:
    results = await aclient.categories.get_all(
        limit=1,
        filters=[
            FilterEntity(field="name", value=CATEGORIES, operator=FilterOperator.IN)
        ],
    )
    category = results[0]

    response = await aclient.categories.get(category_id=category.id)

    assert response.id == category.id
    assert response.deprecated == category.deprecated
    assert response.name == category.name
    assert response.color == category.color
    assert response.icon_text == category.icon_text
