import datetime
from django.conf import settings
from django.core.cache import cache
from django.contrib.gis.geoip2 import GeoIP2

from .models import TrafficFilter, BlockedTrafficEvent
from .utils import get_client_ip

BOT_KEYWORDS = ["bot", "spider", "crawler", "curl", "wget", "python-requests"]


def apply_filters(request_like, campaign):
    """Возвращает True, если трафик допускается."""
    try:
        tf = campaign.traffic_filter
    except TrafficFilter.DoesNotExist:
        tf = TrafficFilter.objects.create(
            campaign=campaign,
            allow_countries=getattr(settings, "TRAFFICFILTER_ALLOWED_COUNTRIES", ["RU", "UA"]),
            ip_rate_limit=getattr(settings, "TRAFFICFILTER_RATE_LIMIT", 60),
        )

    ip = get_client_ip(request_like)
    user_agent = request_like.META.get("HTTP_USER_AGENT", "")

    country = ""
    try:
        g = GeoIP2()
        country = g.country(ip)["country_code"]
    except Exception:
        pass

    reason = None
    if tf.allow_countries and country not in tf.allow_countries:
        reason = "GEO"
    elif ip_in_list(ip, tf.block_ip_list):
        reason = "IP"
    elif tf.block_bots and any(k in user_agent.lower() for k in BOT_KEYWORDS):
        reason = "BOT"
    elif rate_exceeded(ip, tf.ip_rate_limit):
        reason = "RATE"

    if reason:
        if getattr(settings, "TRAFFICFILTER_LOG_BLOCKS", True):
            BlockedTrafficEvent.objects.create(
                campaign=campaign,
                ip=ip or "0.0.0.0",
                country=country,
                user_agent=user_agent,
                reason=reason,
            )
        return False, reason

    return True, None


def ip_in_list(ip, ip_list):
    from ipaddress import ip_address, ip_network
    for net in ip_list or []:
        try:
            if ip_address(ip) in ip_network(net, strict=False):
                return True
        except ValueError:
            continue
    return False


def rate_exceeded(ip, limit):
    now = datetime.datetime.utcnow()
    key = f"tf_rate:{ip}:{now.strftime('%Y%m%d%H%M')}"
    hits = cache.get(key, 0)
    if hits >= limit:
        return True
    cache.set(key, hits + 1, timeout=60)
    return False
