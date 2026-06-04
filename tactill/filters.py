from enum import StrEnum
from typing import Any, Self

from pydantic import BaseModel, model_validator


class FilterOperator(StrEnum):
    EQ = ""
    GT = "[gt]"
    GTE = "[gte]"
    LT = "[lt]"
    LTE = "[lte]"
    NE = "[ne]"
    IN = "[in]"
    NIN = "[nin]"


class FilterEntity(BaseModel):
    field: str
    value: Any
    operator: FilterOperator = FilterOperator.EQ

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        if self.operator in {FilterOperator.IN, FilterOperator.NIN}:
            if not isinstance(self.value, list):
                raise ValueError("Value must be a list")

            if len(self.value) == 0:
                raise ValueError("Value must contain at least one element")

        elif isinstance(self.value, list):
            raise ValueError("Value must not be a list")

        return self

    @property
    def operator_map(self) -> dict[FilterOperator, FilterOperator]:
        return {
            FilterOperator.IN: FilterOperator.EQ,
            FilterOperator.NIN: FilterOperator.NE,
        }

    @property
    def param(self) -> str:
        if self.operator in {FilterOperator.IN, FilterOperator.NIN}:
            if len(self.value) > 1:
                return "&".join(
                    f"{self.field}{self.operator}={value}" for value in self.value
                )
            return f"{self.field}{self.operator_map[self.operator]}={self.value[0]}"

        return f"{self.field}{self.operator}={self.value}"


def build_filters(filters: list[FilterEntity]) -> str:
    return "&".join(filter_.param for filter_ in filters)
