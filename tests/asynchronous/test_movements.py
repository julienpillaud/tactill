import datetime

import pytest

from tactill import AsyncTactillClient, FilterEntity, FilterOperator, TactillUUID
from tactill.entities.movement import (
    ArticleMovement,
    Movement,
    MovementCreate,
    MovementMotive,
    MovementState,
    MovementType,
)


@pytest.mark.skip_on_ci
@pytest.mark.asyncio
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


@pytest.mark.skip_on_ci
@pytest.mark.asyncio
async def test_create_movement(
    aclient: AsyncTactillClient,
    article_id: TactillUUID,
) -> None:
    article = await aclient.articles.get(article_id=article_id)
    category = await aclient.categories.get(category_id=article.category_id)

    current_date = datetime.datetime.now(datetime.UTC)

    movement_create = MovementCreate(
        type=MovementType.IN,
        state=MovementState.DONE,
        motive=MovementMotive.TRANSFER,
        movements=[
            ArticleMovement(
                article_id=article_id,
                article_name=article.name,
                category_name=category.name,
                state=MovementState.DONE,
                units=1,
                done_on=current_date,
            )
        ],
    )
    result = await aclient.movements.create(movement_create)
    assert result
