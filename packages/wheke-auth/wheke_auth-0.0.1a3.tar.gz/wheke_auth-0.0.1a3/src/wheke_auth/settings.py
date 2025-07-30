from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    auth_db: str = "db/auth.json"
    secret_key: SecretStr = SecretStr("change_me")
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_prefix="wheke_auth_", env_file=".env", env_file_encoding="utf-8"
    )


auth_settings = AuthSettings()
