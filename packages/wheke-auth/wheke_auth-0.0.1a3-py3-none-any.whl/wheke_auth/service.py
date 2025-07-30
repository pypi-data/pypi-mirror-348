from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from svcs import Container
from svcs.fastapi import DepContainer
from wheke import get_service

from wheke_auth.exceptions import AuthException
from wheke_auth.models import Token, TokenData, User, UserInDB
from wheke_auth.repository import AuthRepository, TinyAuthRepository
from wheke_auth.settings import AuthSettings, auth_settings

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    settings: AuthSettings
    repository: AuthRepository

    def __init__(self, settings: AuthSettings) -> None:
        self.settings = settings
        self.repository = TinyAuthRepository(self.settings.auth_db)

    def decode_access_token_data(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(
                token,
                self.settings.secret_key.get_secret_value(),
                algorithms=[ALGORITHM],
            )
            username: str | None = payload.get("sub")

            if username is None:
                raise AuthException

            return TokenData(username=username)
        except JWTError as ex:
            raise AuthException from ex

    def create_access_token(self, data: dict) -> Token:
        to_encode = data.copy()
        expiration = datetime.now(tz=UTC) + timedelta(
            minutes=self.settings.access_token_expire_minutes
        )
        to_encode.update({"exp": expiration})
        encoded_jwt = jwt.encode(
            to_encode, self.settings.secret_key.get_secret_value(), algorithm=ALGORITHM
        )

        return Token(access_token=encoded_jwt, token_type="bearer")

    async def authenticate_user(self, username: str, password: str) -> UserInDB | None:
        user = await self.get_user(username)

        if user and pwd_context.verify(password, user.hashed_password):
            return user

        return None

    async def get_user(self, username: str) -> UserInDB | None:
        return await self.repository.get_user(username)

    async def create_user(self, user: User, password: str) -> None:
        user = UserInDB(
            hashed_password=pwd_context.hash(password), **(user.model_dump())
        )
        await self.repository.create_user(user)


def auth_service_factory(_: Container) -> AuthService:
    return AuthService(auth_settings)


def get_auth_service(container: DepContainer) -> AuthService:
    return get_service(container, AuthService)


AuthServiceInjection = Annotated[AuthService, Depends(get_auth_service)]
