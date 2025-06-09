from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count, F, Subquery, OuterRef, DecimalField, ExpressionWrapper
from datetime import datetime, timedelta
from .models import Tag, Campaign, TrafficPath, CampaignVariant, CampaignStat, CampaignHeadline, CampaignNote, TeaserMetric
from .serializers import TagSerializer, CampaignSerializer, TrafficPathSerializer, CampaignVariantSerializer, CampaignStatSerializer, CampaignHeadlineSerializer, CampaignNoteSerializer, TeaserMetricCurrentSerializer, TeaserMetricDeltaSerializer
import random
from django_filters import rest_framework as df
from rest_framework.generics import ListAPIView

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

    def get_queryset(self):
        if self.action == "list":
            return super().get_queryset().annotate(variants_count=Count("variants"))
        return super().get_queryset()

    @action(detail=True, methods=["get"])
    def stats(self, request, pk=None):
        date_from_raw = request.GET.get("from") or ""
        date_to_raw   = request.GET.get("to")   or ""

        try:
            date_from = (
                datetime.fromisoformat(date_from_raw)
                if date_from_raw else datetime.utcnow() - timedelta(days=29)
            )
            date_to = (
                datetime.fromisoformat(date_to_raw)
                if date_to_raw else datetime.utcnow()
            )
        except (ValueError, TypeError):
            # 400, а не 500 — клиенту понятно, в чём он ошибся
            return Response({"detail": "Use YYYY-MM-DD"}, status=400)

        if date_to < date_from:        # защитим себя от отрицательного delta
            date_from, date_to = date_to, date_from

        data = []
        for i in range((date_to - date_from).days + 1):
            d = date_from + timedelta(days=i)
            data.append({
                "date": d.date().isoformat(),
                "clicks": random.randint(50, 150),
                "conversions": random.randint(5, 20),
            })
        return Response(data)

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

class StatFilter(df.FilterSet):
    campaign = df.NumberFilter(field_name="campaign_id")
    date     = df.DateFilter()
    hour = df.NumberFilter()

    class Meta:
        model  = CampaignStat
        fields = ["campaign", "date", "hour"]

class CampaignStatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CampaignStat.objects.all()
    serializer_class = CampaignStatSerializer
    filterset_fields = ["campaign", "date", "hour"]
    filterset_class  = StatFilter 
    ordering = ["date", "hour"]

class CampaignHeadlineViewSet(viewsets.ModelViewSet):
    queryset = CampaignHeadline.objects.all()
    serializer_class = CampaignHeadlineSerializer

class CampaignNoteViewSet(viewsets.ModelViewSet):
    queryset = CampaignNote.objects.all()
    serializer_class = CampaignNoteSerializer

# --- 1. текущий срез ---
class TeaserCurrentView(ListAPIView):
    """
    GET /api/teasers/current/?campaign=<id>
    """
    serializer_class = TeaserMetricCurrentSerializer

    def get_queryset(self):
        camp_id = self.request.query_params.get("campaign")
        return TeaserMetric.objects.filter(campaign_id=camp_id)

# --- 2. разница двух последних срезов ---
class TeaserDeltaView(ListAPIView):
    """
    GET /api/teasers/delta/?campaign=<id>
    """
    serializer_class = TeaserMetricDeltaSerializer

    def get_queryset(self):
        camp_id = self.request.query_params.get("campaign")

        # под-запрос для «предыдущего» updated_at
        prev_qs = (
            TeaserMetric.objects
            .filter(campaign_id=camp_id,
                    teaser_id=OuterRef("teaser_id"))
            .order_by("-updated_at")          # самое свежее первое
            .values("clicks", "revenue")[1:2] # берём 2-ю запись
        )

        return (
            TeaserMetric.objects
            .filter(campaign_id=camp_id)
            .order_by("teaser_id", "-updated_at")
            .distinct("teaser_id")             # берём только самый новый срез
            .annotate(
                clicks_prev   = Subquery(prev_qs.values("clicks")),
                revenue_prev  = Subquery(prev_qs.values("revenue")),
                diff_clicks   = F("clicks")   - F("clicks_prev"),
                diff_revenue  = F("revenue")  - F("revenue_prev"),
                roi_now       = ExpressionWrapper(
                                  (F("revenue") - F("cost")) * 100.0 / F("cost"),
                                  output_field=DecimalField(max_digits=7, decimal_places=2)
                               ),
                roi_prev      = ExpressionWrapper(
                                  (F("revenue_prev") - F("cost")) * 100.0 / F("cost"),
                                  output_field=DecimalField(max_digits=7, decimal_places=2)
                               ),
                diff_roi      = F("roi_now") - F("roi_prev")
            )
        )