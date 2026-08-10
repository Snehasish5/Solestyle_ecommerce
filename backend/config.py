from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    mongodb_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_days: int = 7
    razorpay_key_id: str
    razorpay_key_secret: str
    app_name: str = "SoleStyle"
    frontend_url: str = "http://127.0.0.1:5500"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent/".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()