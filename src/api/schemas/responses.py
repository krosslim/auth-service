from pydantic import BaseModel, Field


class AuthResponse(BaseModel):
    access_token: str = Field(
        ...,
        description="Access token",
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30"
        ],
    )
    refresh_token: str = Field(
        ...,
        description="Refresh token",
        examples=["o/jR5QlyuGRl6bIHigHU8sawqJ4yHH1F+Q4SuDpcbhE="],
    )
    token_type: str = Field(..., description="Token type", examples=["Bearer"])


class ErrorResponse(BaseModel):
    code: str = Field(..., description="Tech error code")
    message: str = Field(..., description="Human-readable error message")
