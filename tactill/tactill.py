import httpx

from tactill.entities.account import Account
from tactill.entities.base import TactillUUID
from tactill.entities.catalog import Article

API_URL = "https://api4.tactill.com/v1"


class ResponseError(Exception):
    pass


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

        :return: A list of Article objects representing the retrieved articles.
        """
        url = f"{API_URL}/catalog/articles"
        params = {"node_id": self.node_id, "limit": limit}
        if skip:
            params["skip"] = skip
        if filter:
            params["filter"] = filter
        if order:
            params["order"] = order

        with httpx.Client(headers=self.headers, params=params) as client:
            response = client.get(url)

        result = response.json()

        if response.status_code != httpx.codes.OK:
            raise ResponseError(result)

        return [Article(**article) for article in result]
