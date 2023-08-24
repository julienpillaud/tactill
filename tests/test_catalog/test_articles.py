import httpx
import pytest

from tactill.entities.article import Article, ArticleCreation, ArticleModification
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
    with pytest.raises(ResponseError) as excinfo:
        client.get_articles(filter="bad")

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"


def test_create_article(client: TactillClient) -> None:
    article_creation = ArticleCreation(
        test=False,
        category_id="5d83c74690924d0008f55d3a",
        taxes=["5d70d4e5be8f9f001195ccc1"],
        name="Test",
        icon_text="TEST",
        summary="This is a new article",
        color="#57DB47",
        full_price=1,
        taxfree_price=0.7,
        barcode="123",
        reference="test",
        in_stock=True,
        ignore_stock=False,
    )
    article = client.create_article(article_creation=article_creation)

    assert article.test == article_creation.test
    assert article.category_id == article_creation.category_id
    assert article.taxes == article_creation.taxes
    assert article.name == article_creation.name
    assert article.icon_text == article_creation.icon_text
    assert article.summary == article_creation.summary
    assert article.color == article_creation.color
    assert article.full_price == article_creation.full_price
    assert article.taxfree_price == article_creation.taxfree_price
    assert article.barcode == article_creation.barcode
    assert article.reference == article_creation.reference
    assert article.in_stock == article_creation.in_stock
    assert article.ignore_stock == article_creation.ignore_stock

    client.delete_article(article.id)


def test_create_article_bad_request(client: TactillClient) -> None:
    article_creation = ArticleCreation(
        category_id="5d83c74690924d0008f55d3a",
        taxes=["5d70d4e5be8f9f001195ccc1"],
        name="",
    )
    with pytest.raises(ResponseError) as excinfo:
        client.create_article(article_creation=article_creation)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
    assert (
        error.message
        == 'child "name" fails because ["name" is not allowed to be empty]'
    )


def test_get_article(client: TactillClient) -> None:
    article_id = "5d85058251301a000790fc9b"
    article = client.get_article(article_id=article_id)

    assert article.id == article_id


def test_get_article_not_found(client: TactillClient) -> None:
    article_id = "1d85058251301a000790fc9b"

    with pytest.raises(ResponseError) as excinfo:
        client.get_article(article_id=article_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.NOT_FOUND
    assert error.error == "Not Found"
    assert error.message == '"article_id" specified in "params" could not be found'


def test_get_article_bad_request(client: TactillClient) -> None:
    article_id = "1"

    with pytest.raises(ResponseError) as excinfo:
        client.get_article(article_id=article_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"


def test_update_article(client: TactillClient, article: Article) -> None:
    article_modification = ArticleModification(
        taxes=["5d70d4e5be8f9f001195ccc1"], name="NEW NAME"
    )

    response = client.update_article(
        article_id=article.id, article_modification=article_modification
    )

    assert response.status_code == httpx.codes.OK
    assert response.message == "article successfully updated"

    article = client.get_article(article_id=article.id)

    assert article.name == article_modification.name


def test_update_article_bad_request(client: TactillClient, article: Article) -> None:
    article_modification = ArticleModification(
        taxes=["5d70d4e5be8f9f001195ccc1"], name=""
    )

    with pytest.raises(ResponseError) as excinfo:
        client.update_article(
            article_id=article.id, article_modification=article_modification
        )

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
