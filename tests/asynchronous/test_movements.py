import datetime

import pytest

from tactill import AsyncTactillClient, FilterEntity, FilterOperator
from tactill.entities.movement import (
    Movement,
)


@pytest.mark.skip_on_ci
@pytest.mark.anyio
async def test_get_movements(aclient: AsyncTactillClient) -> None:
    results = await aclient.movements.get_all(
        filters=[
            FilterEntity(
                field="created_at",
                value=datetime.datetime(2026, 1, 1),
                operator=FilterOperator.GT,
            )
        ]
    )

    for result in results:
        assert isinstance(result, Movement)
        assert result.deprecated is False
