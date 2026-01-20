import hashlib
import hmac
import json
import time
from urllib.parse import parse_qsl

from src.domain.models.telegram import TelegramInitDataPayload
from src.domain.providers.auth_provider import AuthProvider, UserInfo
from src.domain.exceptions import AuthProviderException


class TelegramAuthProvider(AuthProvider):
    def __init__(self, bot_token: str, init_data_lifetime: int, exc_code: str = "TELEGRAM_AUTH"):
        self.bot_token = bot_token
        self.init_data_lifetime = init_data_lifetime
        self.exc_code = exc_code

    async def authenticate(self, payload: object) -> UserInfo:
        if not isinstance(payload, TelegramInitDataPayload):
            raise AuthProviderException(code=self.exc_code, message="Invalid request payload")

        try:
            pairs = self._parse_pairs(payload.init_data)
        except ValueError:
            raise AuthProviderException(code=self.exc_code, message="Invalid InitData format")

        data = dict(pairs)
        received_hash = data.get("hash")
        if not received_hash:
            raise AuthProviderException(code=self.exc_code, message="hash in InitData is required")

        if not self._validate(pairs, received_hash, self.bot_token):
            raise AuthProviderException(code=self.exc_code, message="Invalid hash")

        auth_date_str = data.get("auth_date")
        if not auth_date_str:
            raise AuthProviderException(code=self.exc_code, message="auth_date is required")

        try:
            auth_date = int(auth_date_str)
        except ValueError as e:
            raise AuthProviderException(code=self.exc_code, message="auth_date must be int") from e

        now = int(time.time())
        if now - auth_date > int(self.init_data_lifetime):
            raise AuthProviderException(code=self.exc_code, message="InitData expired")

        user_raw = data.get("user")
        if not user_raw:
            raise AuthProviderException(code=self.exc_code, message="user is required")

        try:
            user = json.loads(user_raw)
        except json.JSONDecodeError as e:
            raise AuthProviderException(code=self.exc_code, message="user must be valid JSON") from e

        user_id = user.get("id")
        if user_id is None:
            raise AuthProviderException(code=self.exc_code, message="user_id is required")

        return UserInfo(provider="telegram", sub=str(user_id))

    @staticmethod
    def _parse_pairs(init_data: str) -> list[tuple[str, str]]:
        return parse_qsl(init_data, keep_blank_values=True, strict_parsing=True)

    @staticmethod
    def _validate(
        pairs: list[tuple[str, str]],
        received_hash: str,
        bot_token: str,
    ) -> bool:
        data_check_pairs = [(k, v) for (k, v) in pairs if k != "hash"]
        data_check_string = "\n".join(
            f"{k}={v}" for (k, v) in sorted(data_check_pairs, key=lambda kv: kv[0])
        )

        secret_key = hmac.new(
            key=b"WebAppData",
            msg=bot_token.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()

        expected_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

        return hmac.compare_digest(expected_hash, received_hash)
