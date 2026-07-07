import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./parcelafacil.db"
    exchange_rate_api_url: str = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    exchange_rate_cache_ttl_seconds: int = 3600

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)


# Railway (and other PaaS) inject DATABASE_URL as an env var.
# In local dev without that var, fall back to SQLite.
_db_url = os.environ.get("DATABASE_URL", "sqlite:///./parcelafacil.db")

# SQLAlchemy requires postgresql:// but Railway sometimes provides postgres://
if _db_url.startswith("postgres://"):
    _db_url = _db_url.replace("postgres://", "postgresql://", 1)

settings = Settings(database_url=_db_url)
