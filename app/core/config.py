from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    app_name: str = "webhook-dvr"
    env: str = "dev"

    database_url: str = "postgresql+psycopg://webhook:webhook@localhost:5432/webhook"

    api_key: str = "dev-secret-key"
    replay_target_url: str = "http://localhost:9000/test"


settings = Settings()
