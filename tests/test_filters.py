import datetime

import pytest

from tactill import FilterEntity, FilterOperator, QueryParams, TactillClient
from tactill.entities import Article


@pytest.mark.parametrize("operator", [FilterOperator.IN, FilterOperator.NIN])
def test_filter_in_nin_without_list(operator) -> None:
    with pytest.raises(ValueError):
        FilterEntity(field="field", value=1, operator=operator)


@pytest.mark.parametrize("operator", [FilterOperator.IN, FilterOperator.NIN])
def test_filter_in_nin_with_empty_list(operator) -> None:
    with pytest.raises(ValueError):
        FilterEntity(field="field", value=[], operator=operator)


@pytest.mark.parametrize(
    "operator",
    [
        FilterOperator.EQ,
        FilterOperator.GT,
        FilterOperator.GTE,
        FilterOperator.LT,
        FilterOperator.LTE,
        FilterOperator.NE,
    ],
)
def test_filter_eq_gt_gte_lt_lte_ne_with_list(operator) -> None:
    with pytest.raises(ValueError):
        FilterEntity(field="field", value=[1, 2], operator=operator)


def test_query_params_in():
    query = QueryParams(
        filters=[
            FilterEntity(
                field="field",
                value=[1, 2],
                operator=FilterOperator.IN,
            )
        ]
    )
    assert query.build()["filter"] == "field[in]=1&field[in]=2"


def test_query_params_in_with_one_value():
    query = QueryParams(
        filters=[
            FilterEntity(
                field="field",
                value=[1],
                operator=FilterOperator.IN,
            )
        ]
    )
    assert query.build()["filter"] == "field=1"


def test_query_params_nin():
    query = QueryParams(
        filters=[
            FilterEntity(
                field="field",
                value=[1, 2],
                operator=FilterOperator.NIN,
            )
        ]
    )
    assert query.build()["filter"] == "field[nin]=1&field[nin]=2"


def test_query_params_nin_with_one_value():
    query = QueryParams(
        filters=[
            FilterEntity(
                field="field",
                value=[1],
                operator=FilterOperator.NIN,
            )
        ]
    )
    assert query.build()["filter"] == "field[ne]=1"


def test_query_params_eq():
    query = QueryParams(
        filters=[
            FilterEntity(
                field="field",
                value=1,
                operator=FilterOperator.EQ,
            )
        ]
    )
    assert query.build()["filter"] == "field=1"


@pytest.mark.parametrize(
    "operator",
    [
        FilterOperator.GT,
        FilterOperator.GTE,
        FilterOperator.LT,
        FilterOperator.LTE,
        FilterOperator.NE,
    ],
)
def test_query_params_gt_gte_lt_lte_ne(operator) -> None:
    query = QueryParams(
        filters=[
            FilterEntity(
                field="field",
                value=1,
                operator=operator,
            )
        ]
    )
    assert query.build()["filter"] == f"field{operator}=1"


@pytest.mark.vcr()
def test_get_articles_by_category_id(
    client: TactillClient,
    articles: list[Article],
) -> None:
    category_ids = [article.category_id for article in articles][:2]
    articles_to_test = [
        article for article in articles if article.category_id in category_ids
    ]

    query = QueryParams(
        limit=5000,
        filters=[
            FilterEntity(field="deprecated", value="false"),
            FilterEntity(field="is_default", value="false"),
            FilterEntity(
                field="category_id",
                value=category_ids,
                operator=FilterOperator.IN,
            ),
        ],
    )
    result = client.get_articles(query=query)

    assert len(result) == len(articles_to_test)


@pytest.mark.vcr()
def test_get_articles_by_name(
    client: TactillClient,
    articles: list[Article],
) -> None:
    article_ref = articles[0]
    articles_to_test = [
        article for article in articles if article.name == article_ref.name
    ]

    query = QueryParams(
        limit=5000,
        filters=[
            FilterEntity(field="deprecated", value="false"),
            FilterEntity(field="is_default", value="false"),
            FilterEntity(field="name", value=article_ref.name),
        ],
    )
    result = client.get_articles(query=query)

    assert len(result) == len(articles_to_test)


@pytest.mark.vcr()
def test_get_articles_by_full_price(
    client: TactillClient,
    articles: list[Article],
) -> None:
    article_ref = articles[0]
    articles_to_test = [
        article for article in articles if article.full_price == article_ref.full_price
    ]

    query = QueryParams(
        limit=5000,
        filters=[
            FilterEntity(field="deprecated", value="false"),
            FilterEntity(field="is_default", value="false"),
            FilterEntity(field="full_price", value=article_ref.full_price),
        ],
    )
    result = client.get_articles(query=query)

    assert len(result) == len(articles_to_test)


@pytest.mark.vcr()
def test_get_articles_by_created_at(
    client: TactillClient,
    articles: list[Article],
) -> None:
    article_ref = articles[430]
    date_ref = article_ref.created_at.date()

    start_date = date_ref - datetime.timedelta(days=2)
    end_date = date_ref + datetime.timedelta(days=2)
    articles_to_test = [
        article
        for article in articles
        if start_date < article.created_at.date() < end_date
    ]

    query = QueryParams(
        limit=5000,
        filters=[
            FilterEntity(field="deprecated", value="false"),
            FilterEntity(field="is_default", value="false"),
            FilterEntity(
                field="created_at",
                value=start_date.isoformat(),
                operator=FilterOperator.GT,
            ),
            FilterEntity(
                field="created_at",
                value=end_date.isoformat(),
                operator=FilterOperator.LT,
            ),
        ],
    )
    result = client.get_articles(query=query)

    assert len(result) == len(articles_to_test)
