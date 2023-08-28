import os
from collections.abc import Iterator

import pytest
from dotenv import load_dotenv

from tactill.entities.article import Article, ArticleCreation
from tactill.entities.category import Category, CategoryCreation
from tactill.entities.discount import Discount, DiscountCreation
from tactill.entities.option import (
    Option,
    OptionCreation,
    OptionList,
    OptionListCreation,
)
from tactill.entities.pack import Pack, PackCreation
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


@pytest.fixture
def option_list(client: TactillClient) -> Iterator[OptionList]:
    option_list_creation = OptionListCreation(
        options=["64e3230e2626360008a8ab07"],
        name="TEST",
        multiple=False,
        mandatory=True,
    )
    new_option_list = client.create_option_list(
        option_list_creation=option_list_creation
    )
    yield new_option_list
    client.delete_option_list(option_list_id=new_option_list.id)


@pytest.fixture
def option(client: TactillClient) -> Iterator[Option]:
    option_creation = OptionCreation(
        name="TEST",
        price=1,
    )
    new_option = client.create_option(option_creation=option_creation)
    yield new_option
    client.delete_option(option_id=new_option.id)


@pytest.fixture
def pack(client: TactillClient) -> Iterator[Pack]:
    pack_creation = PackCreation(
        articles=["5d85058251301a000790fc9b"],
        full_price=1,
        taxes=[],
        discounts=[],
    )
    new_pack = client.create_pack(pack_creation=pack_creation)
    yield new_pack
    client.delete_pack(pack_id=new_pack.id)
