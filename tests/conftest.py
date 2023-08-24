import os
from collections.abc import Iterator

import pytest
from dotenv import load_dotenv

from tactill.entities.article import Article, ArticleCreation
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
    )
    new_article = client.create_article(article_creation)
    yield new_article
    client.delete_article(new_article.id)
