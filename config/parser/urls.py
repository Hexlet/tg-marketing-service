from django.urls import path
from . import views

app_name = 'parser'

urlpatterns = [
    # Старые пути для рендеринга Django шаблонов (пока оставим)
    path('channels/list/', views.ParserListView.as_view(), name='list'),
    path('channels/<int:pk>/', views.ParserDetailView.as_view(), name='detail'),
    path('parse/', views.ParserView.as_view(), name='parser'),

    # Новый путь для страницы поиска, использующей Inertia
    path('channels/search/', views.ChannelSearchView.as_view(), name='channel_search'),
]
