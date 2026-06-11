from typing import Any

from pydantic import BaseModel, model_validator

from tactill.entities.base import TactillUUID


class Account(BaseModel):
    node_id: TactillUUID
    company_id: TactillUUID

    @model_validator(mode="before")
    @classmethod
    def validate_model(cls, data: Any) -> Any:  # noqa: ANN401 (can be anything before validation)
        account = {}
        try:
            account["node_id"] = data["nodes"][0]
            account["company_id"] = data["companies"][0]
        except KeyError, IndexError:
            raise ValueError("Validation error") from None

        return account
