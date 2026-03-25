import pytest

from tactill import FilterEntity, FilterOperator, QueryParams, TactillClient
from tactill.data import CATEGORIES
from tactill.entities import Category


@pytest.mark.skip_on_ci
def test_get_all_categories(client: TactillClient) -> None:
    query = QueryParams(limit=1000)
    results = client.get_categories(query=query)

    for result in results:
        assert isinstance(result, Category)


@pytest.mark.skip_on_ci
def test_get_categories(client: TactillClient) -> None:
    query = QueryParams(
        limit=len(CATEGORIES),
        filters=[
            FilterEntity(field="deprecated", value="false"),
            FilterEntity(field="is_default", value="false"),
            FilterEntity(field="name", value=CATEGORIES, operator=FilterOperator.IN),
        ],
    )
    results = client.get_categories(query=query)

    assert len(results) == len(CATEGORIES)
    for result in results:
        assert result.deprecated is False
        assert result.name in CATEGORIES
