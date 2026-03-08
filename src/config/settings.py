from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    SECRET_KEY: str = "super-secret-key-that-is-at-least-32-bytes"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


settings = Settings()
