from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./parcelafacil.db"
    exchange_rate_api_url: str = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    exchange_rate_cache_ttl_seconds: int = 3600

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)


settings = Settings(database_url="sqlite:///./parcelafacil.db")
