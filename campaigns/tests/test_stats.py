from rest_framework.test import APIClient
from django.utils import timezone
from campaigns.models import Campaign
import pytest

pytestmark = pytest.mark.django_db

def test_stats_endpoint():
    c = Campaign.objects.create(name="Test", total_clicks=100, total_conversions=5)
    client = APIClient()
    res = client.get(f"/api/campaigns/{c.id}/stats/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
