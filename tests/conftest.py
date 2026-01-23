import os

import pytest
from dotenv import load_dotenv

from tactill import FilterEntity, QueryParams, TactillClient
from tactill.entities.catalog.article import Article
from tactill.entities.catalog.category import Category
from tactill.entities.catalog.discount import Discount
from tactill.entities.catalog.option import (
    Option,
    OptionList,
)
from tactill.entities.catalog.pack import Pack
from tactill.entities.catalog.tax import Tax

load_dotenv()


@pytest.fixture(scope="session")
def api_key() -> str:
    if key := os.getenv("TACTILL_API_KEY"):
        return key

    raise ValueError("Missing API key")


@pytest.fixture(scope="session")
def client(api_key: str) -> TactillClient:
    return TactillClient(api_key=api_key)


@pytest.fixture(scope="session")
def vcr_config() -> dict[str, list[tuple[str, str]]]:
    return {"filter_headers": [("x-api-key", "*****")]}


@pytest.fixture(scope="session")
def base_query() -> QueryParams:
    return QueryParams(
        filters=[
            FilterEntity(field="deprecated", value="false"),
            FilterEntity(field="is_default", value="false"),
        ]
    )


@pytest.fixture(scope="session")
def articles(client: TactillClient, base_query: QueryParams) -> list[Article]:
    base_query.limit = 5000
    return client.get_articles(query=base_query)


@pytest.fixture(scope="session")
def article(client: TactillClient, base_query: QueryParams) -> Article:
    return client.get_articles(query=base_query)[0]


@pytest.fixture(scope="session")
def category(client: TactillClient, base_query: QueryParams) -> Category:
    return client.get_categories(query=base_query)[0]


@pytest.fixture
def discount(client: TactillClient) -> Discount:
    return client.get_discounts()[0]


@pytest.fixture
def option_list(client: TactillClient) -> OptionList:
    return client.get_option_lists()[0]


@pytest.fixture
def option(client: TactillClient) -> Option:
    return client.get_options()[0]


@pytest.fixture
def pack(client: TactillClient) -> Pack:
    return client.get_packs()[0]


@pytest.fixture
def tax(client: TactillClient, base_query: QueryParams) -> Tax:
    return client.get_taxes(query=base_query)[0]
