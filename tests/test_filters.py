import pytest

from tactill import FilterEntity, FilterOperator
from tactill.filters import build_filters


@pytest.mark.parametrize("operator", [FilterOperator.IN, FilterOperator.NIN])
def test_filter_in_nin_without_list(operator: FilterOperator) -> None:
    with pytest.raises(ValueError):
        FilterEntity(field="field", value=1, operator=operator)


@pytest.mark.parametrize("operator", [FilterOperator.IN, FilterOperator.NIN])
def test_filter_in_nin_with_empty_list(operator: FilterOperator) -> None:
    with pytest.raises(ValueError):
        FilterEntity(field="field", value=[], operator=operator)


@pytest.mark.parametrize(
    "operator",
    [
        FilterOperator.EQ,
        FilterOperator.GT,
        FilterOperator.GTE,
        FilterOperator.LT,
        FilterOperator.LTE,
        FilterOperator.NE,
    ],
)
def test_filter_eq_gt_gte_lt_lte_ne_with_list(operator: FilterOperator) -> None:
    with pytest.raises(ValueError):
        FilterEntity(field="field", value=[1, 2], operator=operator)


def test_filters_params_in() -> None:
    filters = [FilterEntity(field="field", value=[1, 2], operator=FilterOperator.IN)]
    assert build_filters(filters) == "field[in]=1&field[in]=2"


def test_filters_params_in_with_one_value() -> None:
    filters = [FilterEntity(field="field", value=[1], operator=FilterOperator.IN)]
    assert build_filters(filters) == "field=1"


def test_filters_params_nin() -> None:
    filters = [FilterEntity(field="field", value=[1, 2], operator=FilterOperator.NIN)]
    assert build_filters(filters) == "field[nin]=1&field[nin]=2"


def test_filters_params_nin_with_one_value() -> None:
    filters = [FilterEntity(field="field", value=[1], operator=FilterOperator.NIN)]
    assert build_filters(filters) == "field[ne]=1"


def test_filters_params_eq() -> None:
    filters = [FilterEntity(field="field", value=1, operator=FilterOperator.EQ)]
    assert build_filters(filters) == "field=1"


@pytest.mark.parametrize(
    "operator",
    [
        FilterOperator.GT,
        FilterOperator.GTE,
        FilterOperator.LT,
        FilterOperator.LTE,
        FilterOperator.NE,
    ],
)
def test_filters_params_gt_gte_lt_lte_ne(operator: FilterOperator) -> None:
    filters = [FilterEntity(field="field", value=1, operator=operator)]
    assert build_filters(filters) == f"field{operator}=1"
