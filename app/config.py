from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_password: str
    jwt_access_token_expire_minutes: int = 30
    jwt_algorithm: str = "HS256"
    jwt_secret_key: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
