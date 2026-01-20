from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.config import settings as s
from src.domain.providers.telegram_auth_provider import TelegramAuthProvider
from src.domain.use_cases.login_use_case import LoginUseCase
from src.storage.postgres.repository.user_repository import UserRepository


class TelegramComponentProvider(Provider):

    component = "telegram"

    @provide(scope=Scope.REQUEST)
    def provide_telegram_auth(self) -> TelegramAuthProvider:
        return TelegramAuthProvider(bot_token=s.telegram.bot_token, init_data_lifetime=s.telegram.init_data_lifetime)

    @provide(scope=Scope.REQUEST)
    def provide_auth_use_case(
            self,
            provider: TelegramAuthProvider,
            session: AsyncSession,
            user_repo: UserRepository
    ) -> LoginUseCase:
        return LoginUseCase(provider, session, user_repo)
