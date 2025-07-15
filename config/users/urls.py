from django.urls import path

from config.users.views import (
    LogoutView,
    LoginView,
    UserProfileView,
    UserRegister,
    UserUpdate,
    AvatarChangeView,
)

app_name = 'users'

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserProfileView.as_view(), name='profile'),
    path('create/', UserRegister.as_view(), name='user_create'),
    path('<slug:username>/avatar-change/', AvatarChangeView.as_view(), name='avatar_update'),
    path('<slug:username>/update/', UserUpdate.as_view(), name='user_update'),
]