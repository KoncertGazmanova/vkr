from django.db import models
from django.conf import settings
from campaigns.models import Campaign

class TrafficFilter(models.Model):
    """Настройки фильтрации трафика для кампании."""
    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE, related_name="traffic_filter")
    allow_countries = models.JSONField(default=list, blank=True)
    block_ip_list = models.JSONField(default=list, blank=True)
    block_bots = models.BooleanField(default=True)
    ip_rate_limit = models.PositiveIntegerField(default=getattr(settings, "TRAFFICFILTER_RATE_LIMIT", 60))

class BlockedTrafficEvent(models.Model):
    """События заблокированного трафика."""
    REASONS = [
        ("BOT", "BOT"),
        ("GEO", "GEO"),
        ("IP", "IP"),
        ("RATE", "RATE"),
    ]
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="blocked_events")
    ip = models.GenericIPAddressField()
    country = models.CharField(max_length=8, blank=True)
    user_agent = models.TextField(blank=True)
    reason = models.CharField(max_length=8, choices=REASONS)
    created_at = models.DateTimeField(auto_now_add=True)
