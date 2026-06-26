from typing import cast

import httpx

from tactill.mixin import ClientMixin
from tactill.synchronous.articles import ArticlesResource
from tactill.synchronous.categories import CategoriesResource
from tactill.synchronous.movements import MovementsResource
from tactill.synchronous.taxes import TaxesResource
from tactill.types import JsonValue, QueryParams


class TactillClient(ClientMixin):
    def __init__(self, api_key: str, http_client: httpx.Client) -> None:
        self._http_client = http_client
        self.headers = {"x-api-key": api_key}
        self.account = self._get_account(headers=self.headers)

        self.articles = ArticlesResource(self)
        self.categories = CategoriesResource(self)
        self.taxes = TaxesResource(self)
        self.movements = MovementsResource(self)

    def request(
        self,
        method: str,
        url: str,
        *,
        params: QueryParams | None = None,
        json: JsonValue | None = None,
    ) -> JsonValue:
        with self._handle_response():
            response = self._http_client.request(
                method,
                url,
                params=params,
                json=json,
                headers=self.headers,
            )
            response.raise_for_status()
            return cast(JsonValue, response.json())
