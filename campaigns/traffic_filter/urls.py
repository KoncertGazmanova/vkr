from rest_framework.routers import DefaultRouter
from .views import TrafficFilterViewSet

router = DefaultRouter()
router.register(r'campaign-filters', TrafficFilterViewSet, basename='campaignfilter')

urlpatterns = router.urls
