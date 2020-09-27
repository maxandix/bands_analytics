from django.urls import path
from . import views

urlpatterns = [
    path('artist/<artist_name>/', views.get_place, name='api-place'),
    path('history/', views.get_history, name='api-history')
]
