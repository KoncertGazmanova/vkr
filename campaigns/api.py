from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime, timedelta
from .models import Tag, Campaign
from .serializers import TagSerializer, CampaignSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

    @action(detail=True, methods=["get"])
    def stats(self, request, pk=None):
        obj = self.get_object()
        date_from = request.GET.get("from")
        date_to = request.GET.get("to")

        try:
            date_from = datetime.fromisoformat(date_from) if date_from else datetime.utcnow() - timedelta(days=29)
            date_to = datetime.fromisoformat(date_to) if date_to else datetime.utcnow()
        except Exception:
            return Response({"error": "invalid date"}, status=400)

        delta = (date_to - date_from).days + 1
        data = []
        for i in range(delta):
            d = date_from + timedelta(days=i)
            data.append({
                "date": d.date().isoformat(),
                "clicks": 50 + i * 2,
                "conversions": (i % 5) + 1
            })
        return Response(data)
