from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./cairn.db"
    api_host: str = "127.0.0.1"
    api_port: int = 8000

    model_config = {"env_file": ".env"}


settings = Settings()
