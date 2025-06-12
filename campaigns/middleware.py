from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from django.core.cache import cache
from geoip2.database import Reader
from django.conf import settings
from .models import BlockedRequest
import datetime

class TrafficFilterMiddleware(MiddlewareMixin):
    """
    Middleware для фильтрации подозрительного трафика.
    Проверяет User-Agent, страну IP и частоту запросов.
    """

    def process_request(self, request):
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        ip = self.get_client_ip(request)
        country = self.get_country(ip)

        # Проверка на бота
        if self.is_bot(user_agent):
            return self.block_request(request, ip, user_agent, country, "BOT")

        # Проверка на страну
        allowed_countries = getattr(settings, "TRAFFICFILTER_ALLOWED_COUNTRIES", ["RU", "UA", "BY", "KZ"])
        if country not in allowed_countries:
            return self.block_request(request, ip, user_agent, country, "GEO")

        # Проверка на частоту запросов
        if self.hit_rate_exceeded(ip):
            return self.block_request(request, ip, user_agent, country, "RATE")

    def block_request(self, request, ip, user_agent, country, reason):
        """Блокирует запрос и логирует, если включено."""
        if getattr(settings, "TRAFFICFILTER_LOG_BLOCKS", True):
            BlockedRequest.objects.create(
                ip=ip,
                user_agent=user_agent,
                country=country,
                reason=reason,
                path=request.path
            )
        return HttpResponseForbidden("Blocked by traffic filter")

    def get_client_ip(self, request):
        """Получает IP-адрес клиента."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")

    def get_country(self, ip):
        """Определяет страну по IP."""
        try:
            reader = Reader(settings.GEOIP_DATABASE)
            return reader.country(ip).country.iso_code
        except Exception:
            return ""

    def is_bot(self, user_agent):
        """Проверяет, является ли User-Agent ботом."""
        bot_keywords = ["bot", "spider", "crawler", "curl", "wget", "python-requests"]
        return any(keyword in user_agent.lower() for keyword in bot_keywords)

    def hit_rate_exceeded(self, ip):
        """Проверяет, превышена ли частота запросов."""
        now = datetime.datetime.now()
        key = f"hits:{ip}:{now.strftime('%Y-%m-%d-%H-%M')}"
        hits = cache.get(key, 0)
        if hits >= getattr(settings, "TRAFFICFILTER_RATE_LIMIT", 60):
            return True
        cache.set(key, hits + 1, timeout=60)
        return False
