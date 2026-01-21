from typing import Annotated, Literal

from pydantic import BaseModel, Field


class TelegramLoginRequest(BaseModel):
    provider: Literal["telegram"]
    init_data: str = Field(
        ...,
        description="Initial data for Telegram auth request",
        examples=["query_id=AAHQI48VAAAAANAjjxWd3mrO&user=%7..."],
    )


LoginRequest = Annotated[
    TelegramLoginRequest,
    Field(discriminator="provider"),
]
