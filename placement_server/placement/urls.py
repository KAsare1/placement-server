from django.urls import path
from .views import (
    ProgramListCreateView, ProgramDetailView,
    ChoiceListCreateView, ChoiceDetailView,
    ResultsListCreateView, ResultsDetailView,
    ConsiderationRequestListCreateView, ConsiderationRequestDetailView,
    PlacementListCreateView, PlacementDetailView, SaveChoiceView, SubmitChoicesView,
)

urlpatterns = [
    path('programs/', ProgramListCreateView.as_view(), name='program-list-create'),
    path('programs/<int:pk>/', ProgramDetailView.as_view(), name='program-detail'),
    
    path('choices/', ChoiceListCreateView.as_view(), name='choice-list-create'),
    path('choices/<int:pk>/', ChoiceDetailView.as_view(), name='choice-detail'),
    path('choices/submit/', SaveChoiceView.as_view(), name='choice-create'),

    path('results/', ResultsListCreateView.as_view(), name='results-list-create'),
    path('results/<int:pk>/', ResultsDetailView.as_view(), name='results-detail'),

    path('considerations/', ConsiderationRequestListCreateView.as_view(), name='consideration-list-create'),
    path('considerations/<int:pk>/', ConsiderationRequestDetailView.as_view(), name='consideration-detail'),

    path('placements/', PlacementListCreateView.as_view(), name='placement-list-create'),
    path('placements/<int:pk>/', PlacementDetailView.as_view(), name='placement-detail'),
]