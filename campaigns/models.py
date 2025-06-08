from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Campaign(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("paused", "Paused"),
        ("stopped", "Stopped"),
    ]

    # базовые
    name = models.CharField(max_length=120, unique=True)
    country = models.CharField(max_length=64, blank=True)
    category = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    started_at = models.DateTimeField(null=True, blank=True)
    stopped_at = models.DateTimeField(null=True, blank=True)

    # статистика
    total_clicks = models.PositiveIntegerField(default=0)
    total_conversions = models.PositiveIntegerField(default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # связи
    tags = models.ManyToManyField(Tag, blank=True, related_name="campaigns")

    def roi(self):
        return (self.total_revenue - self.total_cost) / self.total_cost * 100 if self.total_cost else 0

    def __str__(self):
        return self.name


class CampaignVariant(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="variants")
    landing_page = models.ForeignKey("campaigns.LandingPage", on_delete=models.CASCADE)
    offer = models.ForeignKey("campaigns.Offer", on_delete=models.CASCADE)
    headline = models.ForeignKey("ai_module.GeneratedHeadline", null=True, blank=True, on_delete=models.SET_NULL)
    preview_image_url = models.URLField(blank=True)

    weight = models.PositiveSmallIntegerField(default=1)
    clicks = models.PositiveIntegerField(default=0)
    conversions = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ("campaign", "landing_page", "offer", "headline")

    def cr(self):
        return self.conversions / self.clicks * 100 if self.clicks else 0


class LandingPage(models.Model):
    url = models.URLField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Offer(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
