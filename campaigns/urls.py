from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import TagViewSet, CampaignViewSet, TrafficPathViewSet, CampaignVariantViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'campaigns', CampaignViewSet)
router.register(r'paths', TrafficPathViewSet, basename='paths')
router.register(r'variants', CampaignVariantViewSet, basename='variants')

urlpatterns = [
    path('', include(router.urls)),

    path('tags/', TagViewSet.as_view({'get': 'list', 'post': 'create'}), name='tags-list-create'),
    path('tags/<int:pk>/', TagViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='tags-detail'),
]
