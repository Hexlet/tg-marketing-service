from django.urls import path
from . import views

app_name = 'parser'

urlpatterns = [
    path('channels/', views.ParserListView.as_view(), name='list'),
    path('channels/<int:pk>/', views.ParserDetailView.as_view(), name='detail'),
    path('parse/', views.ParserView.as_view(), name='parser'),
    
    # API URLs
    path('api/v1/channels/search/', views.ChannelSearchView.as_view(), name='api_channel_search'),
]