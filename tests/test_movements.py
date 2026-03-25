import pytest

from tactill import QueryParams, TactillClient
from tactill.entities import Movement


@pytest.mark.skip_on_ci
def test_get_all_movements(client: TactillClient) -> None:
    query = QueryParams(limit=10000)
    results = client.get_movements(query=query)

    for result in results:
        assert isinstance(result, Movement)
