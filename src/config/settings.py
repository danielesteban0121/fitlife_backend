from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jwt_secret_key: str = "supersecretkey_that_is_at_least_32_characters_long_123"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60


settings = Settings()