from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "shouji-sms"
    api_prefix: str = "/api"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/shouji"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret_key: str = "change-this-secret"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24
    admin_email: str | None = None
    admin_password: str | None = None
    frontend_origin: str = "http://localhost:5173"

    class Config:
        env_file = ".env"


settings = Settings()
