class DomainException(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(self.message)

class AuthProviderException(DomainException):
    """Ошибка аутентификации через внешнего провайдера"""

