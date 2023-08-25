import os
from collections.abc import Iterator

import pytest
from dotenv import load_dotenv

from tactill.entities.article import Article, ArticleCreation
from tactill.entities.category import Category, CategoryCreation
from tactill.entities.discount import Discount, DiscountCreation
from tactill.tactill import TactillClient

load_dotenv()


@pytest.fixture
def api_key() -> str:
    if key := os.getenv("API_KEY"):
        return key

    raise ValueError("Missing API key")


@pytest.fixture
def client(api_key: str) -> TactillClient:
    return TactillClient(api_key=api_key)


@pytest.fixture
def article(client: TactillClient) -> Iterator[Article]:
    article_creation = ArticleCreation(
        category_id="5d83c74690924d0008f55d3a",
        taxes=["5d70d4e5be8f9f001195ccc1"],
        name="TEST",
        full_price=1,
        in_stock=True,
    )
    new_article = client.create_article(article_creation=article_creation)
    yield new_article
    client.delete_article(article_id=new_article.id)


@pytest.fixture
def category(client: TactillClient) -> Iterator[Category]:
    category_creation = CategoryCreation(name="TEST")
    new_category = client.create_category(category_creation=category_creation)
    yield new_category
    client.delete_category(category_id=new_category.id)


@pytest.fixture
def discount(client: TactillClient) -> Iterator[Discount]:
    discount_creation = DiscountCreation(name="TEST")
    new_discount = client.create_discount(discount_creation=discount_creation)
    yield new_discount
    client.delete_discount(discount_id=new_discount.id)
