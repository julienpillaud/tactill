from enum import StrEnum
from typing import Any, Self

from pydantic import BaseModel, model_validator


class FilterOperator(StrEnum):
    EQ = ""
    GT = "[gt]"
    GTE = "[gte]"
    LT = "[lt]"
    LTE = "[lte]"
    IN = "[in]"
    NIN = "[nin]"


class FilterEntity(BaseModel):
    field: str
    value: Any
    operator: FilterOperator = FilterOperator.EQ

    @model_validator(mode="after")
    def validate(self) -> Self:
        if self.operator in {
            FilterOperator.IN,
            FilterOperator.NIN,
        } and not isinstance(self.value, list):
            raise ValueError("Value must be a list for IN/NIN operators")
        return self

    @property
    def param(self) -> str:
        if self.operator in {FilterOperator.IN, FilterOperator.NIN}:
            return "&".join(
                f"{self.field}{self.operator}={value}" for value in self.value
            )
        return f"{self.field}{self.operator}={self.value}"


class QueryParams(BaseModel):
    limit: int = 100
    skip: int = 0
    filters: list[FilterEntity] | None = None
    order: str | None = None

    def add_filters(self, filters: list[FilterEntity]) -> None:
        self.filters = self.filters or []
        self.filters.extend(filters)

    def build(self, extra_params: dict[str, str] | None = None) -> dict[str, str]:
        params: dict[str, Any] = {"limit": self.limit}
        if self.skip:
            params["skip"] = self.skip
        if self.filters:
            params["filter"] = "&".join(filter_.param for filter_ in self.filters)
        if self.order:
            params["order"] = self.order
        if extra_params:
            params |= extra_params
        return params
