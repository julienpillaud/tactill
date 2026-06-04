from collections.abc import AsyncIterator, Iterator

import pytest
import pytest_asyncio
from _pytest.nodes import Item
from pydantic_settings import BaseSettings, SettingsConfigDict

from tactill import AsyncTactillClient, TactillClient, TactillUUID


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    api_key: str
    local_test: bool = False


settings = Settings()  # ty:ignore[missing-argument]


def pytest_collection_modifyitems(items: list[Item]) -> None:
    if not settings.local_test:
        skip_on_ci = pytest.mark.skip(reason="Disabled on CI")
        for item in items:
            if "skip_on_ci" in item.keywords:
                item.add_marker(skip_on_ci)


@pytest.fixture(scope="session")
def article_id() -> TactillUUID:
    return "6a2110884d74f3bde34643fc"


@pytest.fixture(scope="session")
def category_id() -> TactillUUID:
    return "6a202c6cbcfe5255c24e1895"


@pytest.fixture(scope="session")
def client() -> Iterator[TactillClient]:
    with TactillClient(api_key=settings.api_key) as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def aclient() -> AsyncIterator[AsyncTactillClient]:
    async with AsyncTactillClient(api_key=settings.api_key) as client:
        yield client
