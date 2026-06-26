from collections.abc import Iterator
from contextlib import contextmanager

import httpx
from httpx import HTTPStatusError
from pydantic import TypeAdapter, ValidationError

from tactill.entities.account import Account
from tactill.exceptions import TactillAPIError, TactillError
from tactill.filters import FilterEntity, build_filters
from tactill.types import JsonValue, QueryParams


class ClientMixin:
    BASE_URL = "https://api4.tactill.com/v1"

    def _get_account(self, headers: dict[str, str]) -> Account:
        with httpx.Client(headers=headers, timeout=3) as client:
            with self._handle_response():
                response = client.get(f"{self.BASE_URL}/account/account")
                response.raise_for_status()
                result = response.json()

        return self._handle_validation(result, response_model=Account)

    @contextmanager
    def _handle_response(self) -> Iterator[None]:
        try:
            yield
        except HTTPStatusError as error:
            raise TactillAPIError(error.response.text) from error
        except Exception as error:
            raise TactillError(str(error)) from error

    @staticmethod
    def _handle_validation[T](value: JsonValue, /, response_model: type[T]) -> T:
        try:
            adapter = TypeAdapter(response_model)
            return adapter.validate_python(value)
        except ValidationError as error:
            raise TactillAPIError(str(error)) from error

    @staticmethod
    def _build_params(
        limit: int = 100,
        skip: int = 0,
        filters: list[FilterEntity] | None = None,
        order: str | None = None,
        deprecated: bool = False,
        extra_params: QueryParams | None = None,
    ) -> QueryParams:
        api_filters = [
            FilterEntity(field="deprecated", value="true" if deprecated else "false")
        ]

        if filters is not None:
            for flt in filters:
                if flt.field == "deprecated":
                    raise TactillError("You should use the 'deprecated' parameter")

            api_filters.extend(filters)

        params: dict[str, str | int] = {
            "limit": limit,
            "filter": build_filters(api_filters),
        }
        if skip:
            params["skip"] = skip
        if order:
            params["order"] = order
        if extra_params:
            params |= extra_params

        return params
