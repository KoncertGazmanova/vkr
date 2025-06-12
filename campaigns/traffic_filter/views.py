from rest_framework import viewsets
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

from campaigns.models import Campaign
from .models import TrafficFilter
from .serializers import TrafficFilterSerializer


class TrafficFilterViewSet(viewsets.ViewSet):
    """Получение и обновление настроек фильтра кампании."""

    def get_object(self, campaign_id):
        campaign = Campaign.objects.get(pk=campaign_id)
        tf, _ = TrafficFilter.objects.get_or_create(
            campaign=campaign,
            defaults={
                "allow_countries": getattr(settings, "TRAFFICFILTER_ALLOWED_COUNTRIES", ["RU", "UA"]),
                "ip_rate_limit": getattr(settings, "TRAFFICFILTER_RATE_LIMIT", 60),
            },
        )
        return tf

    def retrieve(self, request, pk=None):
        tf = self.get_object(pk)
        return Response(TrafficFilterSerializer(tf).data)

    def update(self, request, pk=None):
        tf = self.get_object(pk)
        serializer = TrafficFilterSerializer(tf, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
