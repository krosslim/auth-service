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


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(
        ...,
        description="Refresh token",
        examples=["o/jR5QlyuGRl6bIHigHU8sawqJ4yHH1F+Q4SuDpcbhE="],
    )
