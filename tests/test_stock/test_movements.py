from tactill import TactillClient
from tactill.entities.catalog.article import Article
from tactill.entities.stock.movement import ArticleMovement, MovementCreation


def test_get_movements(client: TactillClient) -> None:
    limit = 10
    movements = client.get_movements(limit=limit)

    assert len(movements) == limit


def test_get_movements_with_skip(client: TactillClient) -> None:
    movements = client.get_movements()
    movements_skip = client.get_movements(skip=1)

    assert movements_skip[0] == movements[1]


def test_get_movements_with_filter(client: TactillClient) -> None:
    movement_number = 2000
    movements = client.get_movements(filter=f"number={movement_number}")

    movement = movements[0]
    assert movement.number == movement_number


def test_create_movement_in(client: TactillClient, article: Article) -> None:
    assert article.category_id
    assert article.name
    article_units = 10
    stock_quantity = article.stock_quantity
    category = client.get_category(article.category_id)
    assert category.name

    article_movement = ArticleMovement(
        article_id=article.id,
        article_name=article.name,
        category_name=category.name,
        state="done",
        units=article_units,
    )
    movement_creation = MovementCreation(
        validated_by=[],
        type="in",
        state="done",
        movements=[article_movement],
    )
    movement = client.create_movement(movement_creation=movement_creation)

    assert movement.validated_by == movement_creation.validated_by
    assert movement.type == movement_creation.type
    assert movement.state == movement_creation.state
    assert movement.movements
    assert movement.movements[0].article_id == article_movement.article_id
    assert movement.movements[0].article_name == article_movement.article_name
    assert movement.movements[0].category_name == article_movement.category_name
    assert movement.movements[0].state == article_movement.state
    assert movement.movements[0].units == article_movement.units

    updated_article = client.get_article(article_id=article.id)
    assert updated_article.stock_quantity == stock_quantity + article_units


def test_create_movement_out(client: TactillClient, article: Article) -> None:
    assert article.category_id
    assert article.name
    article_units = 10
    stock_quantity = article.stock_quantity
    category = client.get_category(article.category_id)
    assert category.name

    article_movement = ArticleMovement(
        article_id=article.id,
        article_name=article.name,
        category_name=category.name,
        state="done",
        units=article_units,
    )
    movement_creation = MovementCreation(
        validated_by=[],
        type="out",
        state="done",
        movements=[article_movement],
    )
    movement = client.create_movement(movement_creation=movement_creation)

    assert movement.validated_by == movement_creation.validated_by
    assert movement.type == movement_creation.type
    assert movement.state == movement_creation.state
    assert movement.movements
    assert movement.movements[0].article_id == article_movement.article_id
    assert movement.movements[0].article_name == article_movement.article_name
    assert movement.movements[0].category_name == article_movement.category_name
    assert movement.movements[0].state == article_movement.state
    assert movement.movements[0].units == article_movement.units

    updated_article = client.get_article(article_id=article.id)
    assert updated_article.stock_quantity == stock_quantity - article_units
