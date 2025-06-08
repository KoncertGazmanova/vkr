from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import TagViewSet, CampaignViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'campaigns', CampaignViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('tags/', TagViewSet.as_view({'get': 'list', 'post': 'create'}), name='tags-list-create'),
    path('tags/<int:pk>/', TagViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='tags-detail'),

    path('campaigns/', CampaignViewSet.as_view({'get': 'list', 'post': 'create'}), name='campaigns-list-create'),
    path('campaigns/<int:pk>/', CampaignViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='campaigns-detail'),
]
