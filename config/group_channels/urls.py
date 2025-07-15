from django.urls import path

from config.group_channels.views import (
    GroupProfileView,
    CreateGroupView,
    UpdateGruopView,
    DeleteGroupView,
)

app_name = 'group_channels'

urlpatterns = [
    path('<slug:name>/show/', GroupProfileView.as_view(), name='group_show'),
    path('<slug:name>/update/', UpdateGruopView.as_view(), name='group_update'),
    path('<slug:name>/delete/', DeleteGroupView.as_view(), name='group_delete'),
    path('create/', CreateGroupView.as_view(), name='group_create'),
]