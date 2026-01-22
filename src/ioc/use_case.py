from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.config import settings as s
from src.domain.providers.telegram_auth_provider import TelegramAuthProvider
from src.domain.use_cases.login_use_case import LoginUseCase
from src.domain.use_cases.token_use_case import TokenUseCase
from src.storage.database.repository.token_repository import TokenRepository
from src.storage.database.repository.user_repository import UserRepository

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


class TelegramComponentProvider(Provider):
    component = "telegram"

    @provide(scope=Scope.REQUEST)
    def provide_telegram_auth(self) -> TelegramAuthProvider:
        return TelegramAuthProvider(
            bot_token=s.telegram.bot_token,
            init_data_lifetime=s.telegram.init_data_lifetime,
        )

    @provide(scope=Scope.REQUEST)
    def provide_auth_use_case(
        self,
        provider: TelegramAuthProvider,
        session: Annotated[AsyncSession, FromComponent("")],
        user_repo: Annotated[UserRepository, FromComponent("")],
        token: Annotated[TokenUseCase, FromComponent("")],
    ) -> LoginUseCase:
        return LoginUseCase(provider, session, user_repo, token)


class TokenUseCaseProvider(Provider):

    @provide(scope=Scope.APP)
    def provide_access_private_key(self) -> rsa.RSAPrivateKey:
        key = serialization.load_pem_private_key(
            s.access_token.private_key_pem,
            password=None,
        )
        if not isinstance(key, rsa.RSAPrivateKey):
            raise TypeError("ACCESS private key is not an RSA private key")
        return key

    @provide(scope=Scope.REQUEST)
    def provide_token_use_case(
        self,
        session: AsyncSession,
        token_repo: TokenRepository,
        access_private_key: rsa.RSAPrivateKey
    ) -> TokenUseCase:
        return TokenUseCase(
            session,
            token_repo,
            access_private_key
        )
