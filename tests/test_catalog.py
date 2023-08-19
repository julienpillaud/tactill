import httpx
import pytest

from tactill.entities.article import ArticleCreation
from tactill.entities.category import CategoryCreation
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
        category_id="5d83c74690924d0008f55d3a",
        taxes=["5d70d4e5be8f9f001195ccc1"],
        name="Test",
        full_price=1,
        barcode="123",
        reference="test",
        in_stock=True,
    )
    article = client.create_article(article_creation=article_creation)

    assert article.category_id == article_creation.category_id
    assert article.taxes == article_creation.taxes
    assert article.name == article_creation.name
    assert article.full_price == article_creation.full_price
    assert article.barcode == article_creation.barcode
    assert article.reference == article_creation.reference
    assert article.in_stock == article_creation.in_stock

    client.delete_article(article.id)


def test_create_article_bad_request(client: TactillClient) -> None:
    article_creation = ArticleCreation(
        category_id="5d83c74690924d0008f55d3a",
        taxes=["5d70d4e5be8f9f001195ccc1"],
        name="",
        full_price=1,
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


def test_get_categories(client: TactillClient) -> None:
    limit = 30
    categories = client.get_categories(limit=limit)

    assert len(categories) == limit


def test_get_categories_with_skip(client: TactillClient) -> None:
    categories = client.get_categories()
    categories_skip = client.get_categories(skip=1)

    assert categories_skip[0] == categories[1]


def test_get_categories_with_filter(client: TactillClient) -> None:
    category_name = "BIÈRE"
    categories = client.get_categories(filter=f"name={category_name}")

    category = categories[0]
    assert category.name == category_name


def test_get_categories_with_order(client: TactillClient) -> None:
    categories = client.get_categories(order="name=ASC")

    names = [category.name for category in categories if category.name]
    sorted_names = sorted(names)
    assert names == sorted_names


def test_get_categories_bad_request(client: TactillClient) -> None:
    with pytest.raises(ResponseError) as excinfo:
        client.get_categories(filter="bad")

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"


def test_create_category(client: TactillClient) -> None:
    category_creation = CategoryCreation(name="Test", icon_text="TEST")
    category = client.create_category(category_creation=category_creation)

    assert category.name == category_creation.name
    assert category.icon_text == category_creation.icon_text

    client.delete_category(category.id)


def test_create_category_bad_request(client: TactillClient) -> None:
    category_creation = CategoryCreation(name="")
    with pytest.raises(ResponseError) as excinfo:
        client.create_category(category_creation=category_creation)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
    assert (
        error.message
        == 'child "name" fails because ["name" is not allowed to be empty]'
    )


def test_get_category(client: TactillClient) -> None:
    category_id = "5d83c74690924d0008f55d3a"
    category = client.get_category(category_id=category_id)

    assert category.id == category_id


def test_get_category_not_found(client: TactillClient) -> None:
    category_id = "1d83c74690924d0008f55d3a"

    with pytest.raises(ResponseError) as excinfo:
        client.get_category(category_id=category_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.NOT_FOUND
    assert error.error == "Not Found"
    assert error.message == '"category_id" specified in "params" could not be found'


def test_get_category_bad_request(client: TactillClient) -> None:
    category_id = "1"

    with pytest.raises(ResponseError) as excinfo:
        client.get_category(category_id=category_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
