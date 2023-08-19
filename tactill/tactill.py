from typing import Any

import httpx

from tactill.entities.account import Account
from tactill.entities.article import Article, ArticleCreation
from tactill.entities.base import TactillResponse, TactillUUID
from tactill.entities.category import Category, CategoryCreation
from tactill.entities.discount import Discount

API_URL = "https://api4.tactill.com/v1"


class ResponseError(Exception):
    def __init__(self, error: httpx.Response):
        super().__init__(error)
        response_error = error.json()
        self.error = TactillResponse(**response_error)


class TactillClient:
    def __init__(self, api_key: TactillUUID) -> None:
        self.headers = {"x-api-key": api_key}
        url = f"{API_URL}/account/account"

        with httpx.Client(headers=self.headers) as client:
            response = client.get(url)

        if response.status_code != httpx.codes.OK:
            raise ConnectionError(response.status_code)

        account = response.json()
        self.account = Account(**account)
        self.node_id = self.account.nodes[0]
        self.company_id = self.account.companies[0]
        self.shop_id = self.account.shops[0]

    def _request(
        self,
        method: str,
        url: str,
        expected_status: httpx.codes,
        params: Any = None,
        json: Any = None,
    ) -> Any:
        with httpx.Client(headers=self.headers) as client:
            response = client.request(method=method, url=url, params=params, json=json)

        if response.status_code != expected_status:
            raise ResponseError(response)

        return response.json()

    def get_articles(
        self,
        limit: int = 100,
        skip: int = 0,
        filter: str | None = None,
        order: str | None = None,
    ) -> list[Article]:
        """
        Get a list of Article based on the given filters.

        :param limit: Limit the number of returned records.
        :param skip: Define an offset in the returned records.
        :param filter: Allow filtering the results based on query language.
        :param order: Allow ordering by field (example "field1=ASC&field2=DESC").

        :return: A list of retrieved articles.
        """
        url = f"{API_URL}/catalog/articles"
        params = {"node_id": self.node_id, "limit": limit}
        if skip:
            params["skip"] = skip
        if filter:
            params["filter"] = filter
        if order:
            params["order"] = order

        response = self._request(
            "GET", url, expected_status=httpx.codes.OK, params=params
        )

        return [Article(**article) for article in response]

    def create_article(self, article_creation: ArticleCreation) -> Article:
        """
        Create a new article.

        :param article_creation: The article creation data.

        :return: The created article.
        """
        url = f"{API_URL}/catalog/articles"
        article = article_creation.model_dump()
        article["node_id"] = self.node_id

        response = self._request(
            "POST", url, expected_status=httpx.codes.CREATED, json=article
        )

        return Article(**response)

    def delete_article(self, article_id: TactillUUID) -> TactillResponse:
        """
        Delete an article.

        :param article_id: The ID of the article to be deleted.

        :return: A `TactillResponse` object representing the response from the API.
        """
        url = f"{API_URL}/catalog/articles/{article_id}"

        response = self._request("DELETE", url, expected_status=httpx.codes.OK)

        return TactillResponse(**response)

    def get_article(self, article_id: TactillUUID) -> Article:
        """
        Get an Article by its unique id.

        :param article_id: The ID of the article.

        :return: The article object with the corresponding ID.
        """
        url = f"{API_URL}/catalog/articles/{article_id}"

        response = self._request("GET", url, expected_status=httpx.codes.OK)

        return Article(**response)

    def get_categories(
        self,
        limit: int = 100,
        skip: int = 0,
        filter: str | None = None,
        order: str | None = None,
    ) -> list[Category]:
        """
        Get a list of Category based on the given filters.

        :param limit: Limit the number of returned records.
        :param skip: Define an offset in the returned records.
        :param filter: Allow filtering the results based on query language.
        :param order: Allow ordering by field (example "field1=ASC&field2=DESC").

        :return: A list of retrieved categories.
        """
        url = f"{API_URL}/catalog/categories"
        params = {"company_id": self.company_id, "limit": limit}
        if skip:
            params["skip"] = skip
        if filter:
            params["filter"] = filter
        if order:
            params["order"] = order

        response = self._request(
            "GET", url, expected_status=httpx.codes.OK, params=params
        )

        return [Category(**article) for article in response]

    def create_category(self, category_creation: CategoryCreation) -> Category:
        """
        Create a new category.

        :param category_creation: The category creation data.

        :return: The created category.
        """
        url = f"{API_URL}/catalog/categories"
        category = category_creation.model_dump()
        category["company_id"] = self.company_id

        response = self._request(
            "POST", url, expected_status=httpx.codes.CREATED, json=category
        )

        return Category(**response)

    def delete_category(self, category_id: TactillUUID) -> TactillResponse:
        """
        Delete a category.

        :param category_id: The ID of the category to be deleted.

        :return: A `TactillResponse` object representing the response from the API.
        """
        url = f"{API_URL}/catalog/categories/{category_id}"

        response = self._request("DELETE", url, expected_status=httpx.codes.OK)

        return TactillResponse(**response)

    def get_category(self, category_id: TactillUUID) -> Category:
        """
        Get a Category by its unique id

        :param category_id: The ID of the category.

        :return: The category object with the corresponding ID.
        """
        url = f"{API_URL}/catalog/categories/{category_id}"

        response = self._request("GET", url, expected_status=httpx.codes.OK)

        return Category(**response)

    def get_discounts(
        self,
        limit: int = 100,
        skip: int = 0,
        filter: str | None = None,
        order: str | None = None,
    ) -> list[Discount]:
        """
        Get a list of Discount based on the given filters.

        :param limit: Limit the number of returned records.
        :param skip: Define an offset in the returned records.
        :param filter: Allow filtering the results based on query language.
        :param order: Allow ordering by field (example "field1=ASC&field2=DESC").

        :return: A list of retrieved discounts.
        """
        url = f"{API_URL}/catalog/discounts"
        params = {"shop_id": self.shop_id, "limit": limit}
        if skip:
            params["skip"] = skip
        if filter:
            params["filter"] = filter
        if order:
            params["order"] = order

        response = self._request(
            "GET", url, expected_status=httpx.codes.OK, params=params
        )

        return [Discount(**article) for article in response]
