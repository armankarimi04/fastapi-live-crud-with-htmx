from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    STATIC_URL: str = "static"
    TEMPLATES_DIR: str = "templates"
    VITE_DEV_MODE: bool

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
        

settings = Settings()