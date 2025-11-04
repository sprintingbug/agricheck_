from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENV: str = "dev"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    CORS_ORIGINS: str = "*"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    @property
    def DATABASE_URL(self) -> str:
        return "sqlite:///./agricheck.db"


settings = Settings()
