from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    cors_allowed_origins: str = "http://localhost:5173"

    class Config:
        env_file = ".env"


settings = Settings()
