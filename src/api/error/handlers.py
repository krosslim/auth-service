from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.api.schemas.responses import ErrorResponse
from src.domain.exceptions import DomainException
from starlette import status


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainException)
    async def domain_exception_handler(_: Request, exc: DomainException):
        body = ErrorResponse(code=exc.code, message=exc.message).model_dump()

        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=body)
