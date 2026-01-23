import pytest

from tactill import FilterEntity, QueryParams, TactillClient
from tactill.entities import Movement


@pytest.mark.vcr()
def test_get_movements(client: TactillClient) -> None:
    limit = 10
    query = QueryParams(limit=limit)
    movements = client.get_movements(query=query)

    assert len(movements) == limit


@pytest.mark.vcr()
def test_get_movements_with_skip(client: TactillClient) -> None:
    movements = client.get_movements()
    query = QueryParams(skip=1)
    movements_skip = client.get_movements(query=query)

    assert movements_skip[0] == movements[1]


@pytest.mark.vcr()
def test_get_movements_with_filter(client: TactillClient, movement: Movement) -> None:
    movement_number = movement.number
    query = QueryParams(filters=[FilterEntity(field="number", value=movement_number)])
    movements = client.get_movements(query=query)

    movement = movements[0]
    assert movement.number == movement_number
