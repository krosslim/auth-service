import base64
import hashlib
import hmac
import json
import secrets
import time
from datetime import UTC, datetime, timedelta
from uuid import UUID

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from src.app.config import settings as s
from src.domain.exceptions import RefreshHashException
from src.domain.models.token import AuthResponseDto, RefreshTokenDto


class TokenUseCase:
    def __init__(self, session, token_repo, private_key: rsa.RSAPrivateKey):
        self.session = session
        self.token_repo = token_repo
        self.private_key = private_key

    async def issue(self, user_id: UUID) -> AuthResponseDto:
        access_token = self._create_access(user_id)
        refresh_token = self._create_refresh()
        refresh_hash = self._create_refresh_hash(refresh_token)
        await self._save_refresh(
            user_id=user_id,
            token_hash=refresh_hash,
            expires_at=datetime.now(tz=UTC)
            + timedelta(seconds=s.refresh_token.TTL_SECONDS),
        )

        return AuthResponseDto(access_token=access_token, refresh_token=refresh_token)

    async def refresh(self, refresh_token: str) -> AuthResponseDto:
        async with self.session.begin():
            refresh_hash = self._create_refresh_hash(refresh_token)

            hash_record = await self._mark_token_as_revoked(refresh_hash)

            return await self.issue(hash_record.user_id)

    async def revoke(self, refresh_token: str) -> None:
        async with self.session.begin():
            refresh_hash = self._create_refresh_hash(refresh_token)

            await self._mark_token_as_revoked(refresh_hash)

            return None

    def _create_access(self, user_id: UUID) -> str:
        now = int(time.time())

        payload: dict[str, object] = {
            "sub": str(user_id),
            "exp": now + s.access_token.TTL_SECONDS,
            "iat": now,
        }

        header: dict[str, object] = {"alg": "RS256", "typ": "JWT"}

        encoded_header = self._b64url_encode_json(header)
        encoded_payload = self._b64url_encode_json(payload)

        signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")

        signature = self.private_key.sign(
            data=signing_input,
            padding=padding.PKCS1v15(),
            algorithm=hashes.SHA256(),
        )

        return (
            f"{encoded_header}.{encoded_payload}.{self._b64url_encode_bytes(signature)}"
        )

    def _create_refresh(self) -> str:
        raw = secrets.token_bytes(32)
        refresh_token = self._b64url_encode_bytes(raw)

        return refresh_token

    async def _save_refresh(
        self, user_id: UUID, token_hash: bytes, expires_at: datetime
    ) -> RefreshTokenDto:
        return await self.token_repo.create(user_id, token_hash, expires_at)

    async def _mark_token_as_revoked(self, refresh_hash: bytes) -> RefreshTokenDto:
        now = datetime.now(tz=UTC)

        hash_record = await self.token_repo.mark_revoked(refresh_hash, now)

        if hash_record is None:
            raise RefreshHashException()

        return hash_record

    @staticmethod
    def _create_refresh_hash(refresh_token: str) -> bytes:
        return hmac.new(
            s.refresh_token.hmac_key, refresh_token.encode("ascii"), hashlib.sha256
        ).digest()

    @staticmethod
    def _b64url_encode_json(data: dict) -> str:
        raw = json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode(
            "utf-8"
        )
        return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")

    @staticmethod
    def _b64url_encode_bytes(raw: bytes) -> str:
        return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")
