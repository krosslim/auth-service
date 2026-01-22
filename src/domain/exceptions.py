class DomainException(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(self.message)


class AuthProviderException(DomainException):
    """Ошибка аутентификации через внешнего провайдера"""


class DuplicateIdentityException(DomainException):
    """Обнаружен дубликат Identity Provider у пользователя"""


class RefreshHashException(DomainException):
    """Хэш токена не найден"""

    DEFAULT_CODE = "UNAUTHORIZED"
    DEFAULT_MESSAGE = "The refresh token is invalid, expired, or revoked"

    def __init__(self, code: str | None = None, message: str | None = None):
        super().__init__(
            code=code or self.DEFAULT_CODE, message=message or self.DEFAULT_MESSAGE
        )
