from pydantic import BaseModel, Field


class TelegramAuthRequest(BaseModel):
    init_data: str = Field(
        ...,
        description="Initial data for Telegram auth request",
        examples=["query_id=AAHQI48VAAAAANAjjxWd3mrO&user=%7..."],
    )
