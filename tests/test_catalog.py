import pytest

from tactill.tactill import ResponseError, TactillClient


def test_get_articles(client: TactillClient) -> None:
    limit = 100
    articles = client.get_articles(limit=limit)

    assert len(articles) == limit


def test_get_articles_with_skip(client: TactillClient) -> None:
    articles = client.get_articles()
    articles_skip = client.get_articles(skip=1)

    assert articles_skip[0] == articles[1]


def test_get_articles_with_filter(client: TactillClient) -> None:
    article_name = "Kwak 33cl"
    articles = client.get_articles(filter=f"name={article_name}")

    article = articles[0]
    assert article.name == article_name


def test_get_articles_with_order(client: TactillClient) -> None:
    articles = client.get_articles(order="name=ASC")

    names = [article.name for article in articles if article.name]
    sorted_names = sorted(names)
    assert names == sorted_names


def test_get_articles_bad_request(client: TactillClient) -> None:
    with pytest.raises(ResponseError):
        client.get_articles(filter="bad")
