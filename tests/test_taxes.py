import pytest

from tactill import FilterEntity, QueryParams, TactillClient
from tactill.data import TAX_RATES
from tactill.entities import Tax


@pytest.mark.skip_on_ci
def test_get_all_taxes(client: TactillClient) -> None:
    query = QueryParams(limit=1000)
    results = client.get_taxes(query=query)

    for result in results:
        assert isinstance(result, Tax)


@pytest.mark.skip_on_ci
def test_get_taxes(client: TactillClient) -> None:
    query = QueryParams(
        limit=len(TAX_RATES),
        filters=[FilterEntity(field="deprecated", value="false")],
    )
    results = client.get_taxes(query=query)

    assert len(results) == len(TAX_RATES)
    for result in results:
        assert result.deprecated is False
        assert result.rate in TAX_RATES
