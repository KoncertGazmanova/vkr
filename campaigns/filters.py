from geoip2.database import Reader
from django.core.cache import cache
import datetime

def get_country(ip):
    """Определяет страну по IP."""
    try:
        reader = Reader(settings.GEOIP_DATABASE)
        return reader.country(ip).country.iso_code
    except Exception:
        return ""

def is_bot(user_agent):
    """Проверяет, является ли User-Agent ботом."""
    bot_keywords = ["bot", "spider", "crawler", "curl", "wget", "python-requests"]
    return any(keyword in user_agent.lower() for keyword in bot_keywords)

def hit_rate_exceeded(ip):
    """Проверяет, превышена ли частота запросов."""
    now = datetime.datetime.now()
    key = f"hits:{ip}:{now.strftime('%Y-%m-%d-%H-%M')}"
    hits = cache.get(key, 0)
    if hits >= getattr(settings, "TRAFFICFILTER_RATE_LIMIT", 60):
        return True
    cache.set(key, hits + 1, timeout=60)
    return False
