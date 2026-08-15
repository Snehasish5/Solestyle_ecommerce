from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    mongodb_url: str
    jwt_secret: str

    jwt_algorithm: str = "HS256"
    access_token_expire_days: int = 7

    razorpay_key_id: str
    razorpay_key_secret: str

    app_name: str = "SoleStyle"

    frontend_url: str = "https://solestylee.netlify.app"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()