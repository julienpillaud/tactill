from collections.abc import Iterator
from contextlib import contextmanager

import httpx2
from pydantic import TypeAdapter, ValidationError

from tactill.exceptions import (
    TactillError,
    TactillRejectedError,
    TactillUnavailableError,
    TactillUnexpectedResponseError,
)
from tactill.filters import FilterEntity, build_filters
from tactill.types import JsonValue, QueryParams


class ClientMixin:
    BASE_URL = "https://api4.tactill.com/v1"

    @staticmethod
    @contextmanager
    def _handle_response() -> Iterator[None]:
        try:
            yield
        except httpx2.HTTPStatusError as error:
            response = error.response
            if error.response.status_code >= httpx2.codes.INTERNAL_SERVER_ERROR:
                raise TactillUnavailableError(
                    f"HTTP Error {response.status_code}"
                ) from error
            raise TactillRejectedError(
                status_code=response.status_code,
                response=response.text,
            ) from error
        except httpx2.HTTPError as error:
            raise TactillUnavailableError(str(error)) from error

    @staticmethod
    def _handle_validation[T](value: JsonValue, /, response_model: type[T]) -> T:
        try:
            adapter = TypeAdapter(response_model)
            return adapter.validate_python(value)
        except ValidationError as error:
            raise TactillUnexpectedResponseError(str(error)) from error

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
