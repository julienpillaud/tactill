import pytest
from _pytest.nodes import Item
from _pytest.python import Metafunc
from pydantic_settings import BaseSettings, SettingsConfigDict

from tactill import TactillClient


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    api_keys: list[str] = []
    local_test: bool = False


settings = Settings()


def pytest_collection_modifyitems(items: list[Item]) -> None:
    if not settings.local_test:
        skip_on_ci = pytest.mark.skip(reason="Disabled on CI")
        for item in items:
            if "skip_on_ci" in item.keywords:
                item.add_marker(skip_on_ci)


def pytest_generate_tests(metafunc: Metafunc) -> None:
    if "client" in metafunc.fixturenames and settings.local_test:
        metafunc.parametrize("api_key", settings.api_keys, scope="session")


@pytest.fixture(scope="session")
def client(api_key: str) -> TactillClient:
    return TactillClient(api_key=api_key)
