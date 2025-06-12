from django.test import TestCase, RequestFactory
from campaigns.models import Campaign
from campaigns.traffic_filter.models import TrafficFilter
from campaigns.traffic_filter.filters import apply_filters
from django.core.cache import cache

class TrafficFilterAPITest(TestCase):
    def setUp(self):
        cache.clear()
        self.factory = RequestFactory()
        self.campaign = Campaign.objects.create(name="Test")
        TrafficFilter.objects.create(
            campaign=self.campaign,
            allow_countries=[],
            block_ip_list=["10.0.0.1"],
            block_bots=True,
            ip_rate_limit=60,
        )

    def make_request(self, ip="1.1.1.1", ua="Mozilla/5.0"):
        request = self.factory.get("/", REMOTE_ADDR=ip, HTTP_USER_AGENT=ua)
        return apply_filters(request, self.campaign)

    def test_bot_user_agent(self):
        allowed, reason = self.make_request(ua="Googlebot")
        self.assertFalse(allowed)
        self.assertEqual(reason, "BOT")

    def test_blocked_ip(self):
        allowed, reason = self.make_request(ip="10.0.0.1")
        self.assertFalse(allowed)
        self.assertEqual(reason, "IP")

    def test_rate_limit_exceeded(self):
        for _ in range(60):
            allowed, _ = self.make_request()
            self.assertTrue(allowed)
        allowed, reason = self.make_request()
        self.assertFalse(allowed)
        self.assertEqual(reason, "RATE")

    def test_valid_request(self):
        allowed, reason = self.make_request()
        self.assertTrue(allowed)
        self.assertIsNone(reason)
