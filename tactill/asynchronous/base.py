from types import TracebackType
from typing import cast

import httpx

from tactill.asynchronous.articles import AsyncArticlesResource
from tactill.asynchronous.categories import AsyncCategoriesResource
from tactill.asynchronous.taxes import AsyncTaxesResource
from tactill.mixin import ClientMixin
from tactill.types import JsonValue, QueryParams


class AsyncTactillClient(ClientMixin):
    def __init__(self, api_key: str, timeout: int = 10) -> None:
        self.headers = {"x-api-key": api_key}
        self._client = httpx.AsyncClient(headers=self.headers, timeout=timeout)
        self.account = self._get_account(headers=self.headers)

        self.articles = AsyncArticlesResource(self)
        self.categories = AsyncCategoriesResource(self)
        self.taxes = AsyncTaxesResource(self)

    async def request(
        self,
        method: str,
        url: str,
        *,
        params: QueryParams | None = None,
        json: JsonValue | None = None,
    ) -> JsonValue:
        with self._handle_response():
            response = await self._client.request(method, url, params=params, json=json)
            response.raise_for_status()
            return cast(JsonValue, response.json())

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncTactillClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        await self.aclose()
