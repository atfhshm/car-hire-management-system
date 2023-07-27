from pydantic_settings import BaseSettings, SettingsConfigDict
from os import urandom


__all__ = ["settings"]


class Settings(BaseSettings):
    db_schema: str = "postgres"
    db_user: str = "postgres"
    db_password: str = "123456789"
    db_host: str = "127.0.0.1"
    db_port: str = "5432"
    db_name: str = "postgres"
    secret_key: str = urandom(40).hex()
    hashing_algorithm: str = "HS256"
    access_token_expiry_minutes: int
    refresh_token_expiry_minutes: int = 30 * 24 * 60

    model_config = SettingsConfigDict(case_sensitive=False, env_file=("./.env",))


settings = Settings()
