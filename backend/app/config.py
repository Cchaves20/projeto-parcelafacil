from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./parcelafacil.db"
    secret_key: str = "change-this-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    exchange_rate_api_url: str = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    exchange_rate_cache_ttl_seconds: int = 3600

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
