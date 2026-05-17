from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('note/<int:pk>/', views.detail, name='detail'),
    path('search/', views.search_notes, name='search'),
    path('api/notes/', views.api_notes, name='api_notes'),
]
