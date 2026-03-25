from pydantic import Field

from tactill.entities.base import BaseTactillModel, TactillUUID


class Account(BaseTactillModel):
    account_id: str | None = None
    profile_id: TactillUUID
    role: TactillUUID | None = None
    fastpass: str | None = Field(None, min_length=4, max_length=4)
    last_connected: str | None = None
    companies: list[str]
    shops: list[str]
    nodes: list[str]
    api_key: str | None = None
    v3_account_id: TactillUUID | None = None
    permissions: list[str] | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
