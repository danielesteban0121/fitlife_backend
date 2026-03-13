from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "MySQLPassword"
    DB_NAME: str = "fitlife_db"

    # JWT
    SECRET_KEY: str = "super-secret-key-that-is-at-least-32-bytes"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


settings = Settings()
