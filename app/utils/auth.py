from datetime import datetime, timedelta

import jwt
import pytz
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import PyJWTError

from app.core.exceptions import AppException
from config import settings

UTC = pytz.UTC
JWT_EXPIRES_IN = str(datetime.now() + timedelta(minutes=5))


class JwtAuthentication(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise AppException.Unauthorized(
                    error_message="invalid authentication scheme"
                )
            return self.decode_token(token=credentials.credentials)

    # noinspection PyMethodMayBeStatic
    def generate_token(self, user_id):
        payload = {"id": user_id, "expires": JWT_EXPIRES_IN}
        token = jwt.encode(
            payload=payload, key=settings.secret_key, algorithm=settings.jwt_algorithm
        )
        return {"access_token": token}

    # noinspection PyMethodMayBeStatic
    def decode_token(self, token: str):
        try:
            decoded_token = jwt.decode(
                jwt=token, key=settings.secret_key, algorithms=[settings.jwt_algorithm]
            )
        except PyJWTError as exc:
            raise AppException.Unauthorized(error_message=f"{exc}")
        token_expiration = datetime.strptime(
            decoded_token.get("expires"), "%Y-%m-%d %H:%M:%S.%f"
        ).replace(tzinfo=UTC)
        if UTC.localize(datetime.now()) > token_expiration:
            raise AppException.ExpiredTokenException(error_message="token has expired")
        return decoded_token.get("id")
