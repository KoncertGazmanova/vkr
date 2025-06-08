# ai_module/urls.py
from django.urls import path
from .views import (
    SectionOptionListCreateView,
    SectionOptionDetailView,
    GeneratedHeadlineListView,
    GeneratedHeadlineDetailView,
    get_headlines_by_section,
    generate_random_headline,
    assemble_best_headline
)

urlpatterns = [
    # SectionOption
    path('sections/', SectionOptionListCreateView.as_view(), name='sections-list-create'),
    path('sections/<int:pk>/', SectionOptionDetailView.as_view(), name='sections-detail'),

    # GeneratedHeadline
    path('headlines/', GeneratedHeadlineListView.as_view(), name='headlines-list-create'),
    path('headlines/<int:pk>/', GeneratedHeadlineDetailView.as_view(), name='headlines-detail'),

    # Доп. методы
    path('headlines/by_section/', get_headlines_by_section, name='headlines-by-section'),
    path('headlines/generate_random/', generate_random_headline, name='generate-random-headline'),
    path('headlines/assemble_best/', assemble_best_headline, name='assemble-best-headline'),
]
