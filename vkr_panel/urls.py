from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/ai/', include('ai_module.urls')),
    path('api/', include('campaigns.urls')),

]
