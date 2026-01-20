from dishka import make_async_container

from .database import DatabaseProvider
from .repository import RepositoryProvider
from .use_case import TelegramComponentProvider

container = make_async_container(
    DatabaseProvider(),
    RepositoryProvider(),
    TelegramComponentProvider()
)
