import pytest

from tactill import QueryParams, TactillClient
from tactill.entities import Article


@pytest.mark.skip_on_ci
def test_get_all_articles(client: TactillClient) -> None:
    query = QueryParams(limit=10000)
    results = client.get_articles(query=query)

    for result in results:
        assert isinstance(result, Article)
