from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.api.schemas.responses import ErrorResponse
from src.domain import exceptions as e
from starlette import status

EXCEPTION_STATUS_MAP: dict[type[e.DomainException], int] = {
    e.AuthProviderException: status.HTTP_400_BAD_REQUEST,
    e.DuplicateIdentityException: status.HTTP_409_CONFLICT,
}


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(e.DomainException)
    async def domain_exception_handler(request: Request, exc: e.DomainException):
        status_code = EXCEPTION_STATUS_MAP.get(type(exc), status.HTTP_400_BAD_REQUEST)

        body = ErrorResponse(code=exc.code, message=exc.message).model_dump()

        return JSONResponse(status_code=status_code, content=body)

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        first_error = exc.errors()[0]
        message = first_error.get("msg", "Invalid request payload")

        body = ErrorResponse(
            code="REQUEST_VALIDATION_ERROR",
            message=message,
        ).model_dump()

        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=body)
