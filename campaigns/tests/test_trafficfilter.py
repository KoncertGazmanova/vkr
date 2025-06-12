from django.test import TestCase, RequestFactory
from django.http import HttpRequest
from campaigns.middleware import TrafficFilterMiddleware
from django.core.cache import cache

class TrafficFilterMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = TrafficFilterMiddleware()

    def test_bot_user_agent(self):
        request = self.factory.get("/", HTTP_USER_AGENT="Googlebot")
        response = self.middleware.process_request(request)
        self.assertEqual(response.status_code, 403)

    def test_blocked_country(self):
        request = self.factory.get("/", REMOTE_ADDR="8.8.8.8")
        response = self.middleware.process_request(request)
        self.assertEqual(response.status_code, 403)

    def test_rate_limit_exceeded(self):
        ip = "127.0.0.1"
        for _ in range(60):
            request = self.factory.get("/", REMOTE_ADDR=ip)
            self.middleware.process_request(request)
        request = self.factory.get("/", REMOTE_ADDR=ip)
        response = self.middleware.process_request(request)
        self.assertEqual(response.status_code, 403)

    def test_valid_request(self):
        request = self.factory.get("/", HTTP_USER_AGENT="Mozilla/5.0", REMOTE_ADDR="127.0.0.1")
        response = self.middleware.process_request(request)
        self.assertIsNone(response)
