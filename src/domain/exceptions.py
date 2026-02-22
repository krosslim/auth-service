class DomainException(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(self.message)


class AuthProviderException(DomainException):
    """Ошибка аутентификации через внешнего провайдера"""


class DuplicateIdentityProviderForUser(DomainException):
    """UNIQUE(user_id, provider): у пользователя уже есть identity этого провайдера"""

    DEFAULT_CODE = "IDENTITY_PROVIDER_ALREADY_LINKED"
    DEFAULT_MESSAGE = "This provider is already linked to the user"

    def __init__(self, code: str | None = None, message: str | None = None):
        super().__init__(
            code=code or self.DEFAULT_CODE,
            message=message or self.DEFAULT_MESSAGE,
        )


class DuplicateIdentity(DomainException):
    """UNIQUE(provider, sub): identity уже существует"""

    DEFAULT_CODE = "IDENTITY_ALREADY_EXISTS"
    DEFAULT_MESSAGE = "This identity is already linked to an account"

    def __init__(self, code: str | None = None, message: str | None = None):
        super().__init__(
            code=code or self.DEFAULT_CODE,
            message=message or self.DEFAULT_MESSAGE,
        )


class RefreshHashException(DomainException):
    """Хэш токена не найден"""

    DEFAULT_CODE = "UNAUTHORIZED"
    DEFAULT_MESSAGE = "The refresh token is invalid, expired, or revoked"

    def __init__(self, code: str | None = None, message: str | None = None):
        super().__init__(
            code=code or self.DEFAULT_CODE, message=message or self.DEFAULT_MESSAGE
        )
