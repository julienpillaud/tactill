import httpx
import pytest

from tactill import Article, ArticleUpdate, AsyncTactillClient, TactillUUID


@pytest.mark.skip_on_ci
@pytest.mark.asyncio
async def test_get_articles(aclient: AsyncTactillClient) -> None:
    results = await aclient.articles.get_all(limit=10000)

    for result in results:
        assert isinstance(result, Article)
        assert result.deprecated is False


@pytest.mark.skip_on_ci
@pytest.mark.asyncio
async def test_get_article(aclient: AsyncTactillClient) -> None:
    results = await aclient.articles.get_all(limit=1)
    article = results[0]

    response = await aclient.articles.get(article_id=article.id)

    assert response.id == article.id
    assert response.deprecated == article.deprecated
    assert response.category_id == article.category_id
    assert response.taxes == article.taxes
    assert response.name == article.name
    assert response.icon_text == article.icon_text
    assert response.color == article.color
    assert response.barcode == article.barcode
    assert response.in_stock == article.in_stock
    assert response.reference == article.reference
    assert response.full_price == article.full_price
    assert response.stock_quantity == article.stock_quantity


@pytest.mark.skip_on_ci
@pytest.mark.asyncio
async def test_update_article(
    aclient: AsyncTactillClient,
    article_id: TactillUUID,
) -> None:
    article = await aclient.articles.get(article_id=article_id)
    name_split, number_split = article.name.split(" - ")
    article_name = f"{name_split} - {int(number_split) + 1}"
    article_price = article.full_price + 1 if article.full_price else None

    data = ArticleUpdate(
        taxes=article.taxes,
        name=article_name,
        color=article.color,
        full_price=article_price,
    )
    response = await aclient.articles.update(article_id=article_id, data=data)

    assert response.status_code == httpx.codes.OK
    assert response.error == ""
    assert response.message == "article successfully updated"
