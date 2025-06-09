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
    name = models.CharField(max_length=120)  # дубликаты разрешены
    country = models.CharField(max_length=64, blank=True)
    category = models.CharField(max_length=120, blank=True)  # увеличиваем лимит
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
    leads      = models.PositiveIntegerField(default=0)
    approvals  = models.PositiveIntegerField(default=0)
    payout     = models.DecimalField(max_digits=8, decimal_places=2, default=0)
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


class TrafficPath(models.Model):
    campaign   = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="paths")
    name       = models.CharField(max_length=200)
    clicks     = models.PositiveIntegerField(default=0)
    conversions= models.PositiveIntegerField(default=0)
    cost       = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    revenue    = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    leads = models.PositiveIntegerField(default=0)
    approvals = models.PositiveIntegerField(default=0)
    payout = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        unique_together = ("campaign", "name")

    def cr(self):
        return (self.conversions / self.clicks * 100) if self.clicks else 0
    
class CampaignStat(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="stats")
    date = models.DateField()
    hour = models.PositiveSmallIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    conversions = models.PositiveIntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def roi(self):
        return (self.revenue - self.cost) / self.cost * 100 if self.cost else 0

    class Meta:
        unique_together = ("campaign", "date", "hour")
        indexes = [
            models.Index(fields=["campaign", "date"]),
            models.Index(fields=["campaign", "date", "hour"]),
        ]

class CampaignHeadline(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="headlines")
    title = models.CharField(max_length=200)
    ctr = models.DecimalField(max_digits=5, decimal_places=2, default=0)

class CampaignNote(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="notes")
    content = models.TextField()
    last_edited = models.DateTimeField(auto_now=True)

class TeaserMetric(models.Model):
    campaign    = models.ForeignKey(
        "Campaign",
        on_delete=models.CASCADE,
        related_name="teasers"
    )
    teaser_id   = models.PositiveIntegerField()
    clicks      = models.PositiveIntegerField(default=0)
    conversions = models.PositiveIntegerField(default=0)
    cost        = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    revenue     = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "campaigns_teasermetric"   # ← Точно имя существующей таблицы
        managed  = False                      # ← Не трогаем её миграциями
        unique_together = ("campaign", "teaser_id")

    def roi(self):
        return (self.revenue - self.cost) / self.cost * 100 if self.cost else 0

    def __str__(self):
        return f"T{self.teaser_id} / camp {self.campaign_id}"
    