from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import TagViewSet, CampaignViewSet, TrafficPathViewSet, CampaignVariantViewSet, CampaignStatViewSet, CampaignHeadlineViewSet, CampaignNoteViewSet, TeaserCurrentView, TeaserDeltaView

router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'campaigns', CampaignViewSet)
router.register(r'paths', TrafficPathViewSet, basename='paths')
router.register(r'variants', CampaignVariantViewSet, basename='variants')
router.register(r'stats', CampaignStatViewSet, basename='stats')
router.register(r'headlines', CampaignHeadlineViewSet, basename='headlines')
router.register(r'notes', CampaignNoteViewSet, basename='notes')

urlpatterns = [
    path('', include(router.urls)),
    # ### TF include traffic filter urls
    path('', include('campaigns.traffic_filter.urls')),

    path('tags/', TagViewSet.as_view({'get': 'list', 'post': 'create'}), name='tags-list-create'),
    path('tags/<int:pk>/', TagViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='tags-detail'),

    path("teasers/current/", TeaserCurrentView.as_view(), name="teasers-current"),
    path("teasers/delta/",  TeaserDeltaView.as_view(),  name="teasers-delta"),
]
