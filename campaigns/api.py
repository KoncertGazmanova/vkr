from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from datetime import datetime, timedelta
from .models import Tag, Campaign, TrafficPath, CampaignVariant
from .serializers import TagSerializer, CampaignSerializer, TrafficPathSerializer, CampaignVariantSerializer
import random

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

    @action(detail=True, methods=["get"])
    def stats(self, request, pk=None):
        return Response([])

class TrafficPathViewSet(viewsets.ModelViewSet):
    queryset = TrafficPath.objects.all()
    serializer_class = TrafficPathSerializer

    @action(detail=False, methods=["post"])
    def bayes(self, request):
        path_ids = request.data.get("path_ids", [])
        return Response([])

class CampaignVariantViewSet(viewsets.ModelViewSet):
    queryset = CampaignVariant.objects.all()
    serializer_class = CampaignVariantSerializer
    def get_queryset(self):
        qs = super().get_queryset()
        campaign_id = self.request.query_params.get("campaign")
        if campaign_id:
            qs = qs.filter(campaign_id=campaign_id)
        return qs