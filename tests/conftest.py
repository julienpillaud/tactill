import os

import pytest
from dotenv import load_dotenv

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
