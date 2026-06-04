from types import TracebackType
from typing import cast

import httpx

from tactill.mixin import ClientMixin
from tactill.synchronous.articles import ArticlesResource
from tactill.synchronous.categories import CategoriesResource
from tactill.synchronous.taxes import TaxesResource
from tactill.types import JsonValue, QueryParams


class TactillClient(ClientMixin):
    def __init__(self, api_key: str, timeout: int = 10) -> None:
        self.headers = {"x-api-key": api_key}
        self._client = httpx.Client(headers=self.headers, timeout=timeout)
        self.account = self._get_account(headers=self.headers)

        self.articles = ArticlesResource(self)
        self.categories = CategoriesResource(self)
        self.taxes = TaxesResource(self)

    def request(
        self,
        method: str,
        url: str,
        *,
        params: QueryParams | None = None,
        json: JsonValue | None = None,
    ) -> JsonValue:
        with self._handle_response():
            response = self._client.request(method, url, params=params, json=json)
            response.raise_for_status()
            return cast(JsonValue, response.json())

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> TactillClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        self.close()
