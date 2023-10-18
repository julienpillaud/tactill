from typing import Literal

QueryOperator = Literal["in", "nin"]


def get_query_filter(
    field: str, values: list[str], query_operator: QueryOperator
) -> str:
    query_marker = "" if len(values) == 1 else f"[{query_operator}]"
    return "&".join(f"{field}{query_marker}={x}" for x in values)
