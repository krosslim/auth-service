from contextlib import asynccontextmanager
from logging import getLogger

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.ioc import container
from src.api.errors.handlers import setup_exception_handlers
from src.api.routers import api_router

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    logger.info("Инициализация приложения...")
    yield
    logger.info("Завершение работы приложения...")
    await app_instance.state.dishka_container.close()
    logger.info("Завершено")


def create_app() -> FastAPI:
    created_app = FastAPI(
        title="Auth-service",
        version="1.0.0",
        lifespan=lifespan,
    )

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

    return created_app


app = create_app()
