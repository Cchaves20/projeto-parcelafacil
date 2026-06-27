import time
from decimal import Decimal

import httpx

from app.config import settings
from app.models.enums import Currency

_cached_rate: Decimal | None = None
_cached_at: float = 0.0

FALLBACK_USD_BRL_RATE = Decimal("5.00")


def get_usd_to_brl_rate() -> Decimal:
    global _cached_rate, _cached_at

    if _cached_rate is not None and time.monotonic() - _cached_at < settings.exchange_rate_cache_ttl_seconds:
        return _cached_rate

    try:
        response = httpx.get(settings.exchange_rate_api_url, timeout=5.0)
        response.raise_for_status()
        data = response.json()
        rate = Decimal(data["USDBRL"]["bid"])
    except (httpx.HTTPError, KeyError, ValueError):
        return _cached_rate if _cached_rate is not None else FALLBACK_USD_BRL_RATE

    _cached_rate = rate
    _cached_at = time.monotonic()
    return rate


def to_brl(amount: Decimal, currency: Currency) -> Decimal:
    if currency == Currency.BRL:
        return amount
    return amount * get_usd_to_brl_rate()
