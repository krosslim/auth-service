import logging
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.exception_handlers import setup_exception_handlers
from src.api.routers import api_router
from src.ioc import container
from src.utils.docs_gen import openapi_postprocess

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    logger.info("Инициализация приложения...")
    yield
    logger.info("Завершение работы приложения...")
    await app_instance.state.dishka_container.close()
    logger.info("Завершено")


def create_app() -> FastAPI:
    created_app = FastAPI(title="Auth-service", version="1.0.0", lifespan=lifespan)

    created_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup_exception_handlers(created_app)

    created_app.include_router(api_router)

    setup_dishka(container=container, app=created_app)

    def custom_openapi():
        if created_app.openapi_schema:
            return created_app.openapi_schema
        schema = FastAPI.openapi(created_app)
        schema = openapi_postprocess(schema)
        created_app.openapi_schema = schema
        return schema

    created_app.openapi = custom_openapi

    return created_app


app = create_app()
