from datetime import timedelta, datetime
from typing import Dict, Optional

from fastapi import Header
from jose import jwt

from config.config import settings


class TokenService:

    def __init__(self):
        self.config = settings.jwt_config
        self.token_type = self.config.AUTH_HEADER_TYPES[0]
        self.secret_key = self.config.SECRET_KEY
        self.access_token_lifetime = self.config.ACCESS_TOKEN_LIFETIME
        self.refresh_token_lifetime = self.config.REFRESH_TOKEN_LIFETIME

    def create_access_token(self, data: Dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + self.config.ACCESS_TOKEN_LIFETIME
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.config.ALGORITHM)
        return encoded_jwt

    def decode(self, token: str):
        if token.startswith(self.config.AUTH_HEADER_TYPES):
            token = token.split(' ')[1]
        return jwt.decode(token, self.secret_key, algorithms=[self.config.ALGORITHM])


class LoadAuthorizationHeader:
    def __call__(self, authorization: str = Header(None)) -> Optional[str]:
        return authorization
