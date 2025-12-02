from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import auth, messages
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.contrib.auth.mixins import AccessMixin


class RoleRequiredMixin(AccessMixin):
    """
    Базовый миксин для проверки ролей.
    Наследуем от AccessMixin для стандартного поведения Django.
    """
    allowed_roles = None  # Обязательно переопределить в дочерних классах
    login_url = 'users:login' # Обязательно переопределить в дочерних классах при необходимости
    next_parameter = '?next='  # Параметр для сохранения начальной страницы
    permission_denied_message = "У вас нет прав для доступа к этой странице"

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request, 'role'):
            # Добавляем определение роли к запросу для удобства
            request.role = self._get_user_role(request)

        if not self._test_role(request):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

    def _get_user_role(self, request):
        """Определяем роль пользователя"""
        if not request.user.is_authenticated:
            return 'guest'
        return getattr(request.user, 'role', 'user')  # Используем свойство role из модели

    def _test_role(self, request):
        """Проверяем соответствие роли"""
        if self.allowed_roles is None:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} требует определения allowed_roles"
            )
        return request.role in self.allowed_roles

    def handle_no_permission(self):
        """Обработка отказа в доступе"""
        if not self.request.user.is_authenticated:
            return self.redirect_to_login() 
        raise PermissionDenied(self.get_permission_denied_message())
    
    def redirect_to_login(self):
        """
        Метод для перенаправления на страницу входа с сохранением начального адреса.
        """
        # выводим сообщение
        messages.add_message(self.request, messages.INFO, self.get_permission_denied_message())
        # Перенаправляем гостей на страницу входа,
        # после аутентификации перенаправляем на первоначальную страницу
        return redirect(f"{reverse(self.login_url)}{self.next_parameter}{self.request.path}")


class GuestRequiredMixin(RoleRequiredMixin):
    """Только для неавторизованных пользователей"""
    allowed_roles = ['guest']
    permission_denied_message = "Эта страница доступна только гостям"


class UserRequiredMixin(RoleRequiredMixin):
    """Для всех авторизованных пользователей"""
    allowed_roles = ['user']
    permission_denied_message = "Требуется авторизация"


class PartnerRequiredMixin(RoleRequiredMixin):
    """Только для активных партнеров"""
    allowed_roles = ['partner']
    permission_denied_message = "Доступ только для партнеров"

    def _test_role(self, request):
        """Дополнительная проверка активного статуса партнера"""
        return (
                super()._test_role(request) and
                hasattr(request.user, 'is_partner') and
                request.user.is_partner
        )


class ChannelModeratorRequiredMixin(RoleRequiredMixin):
    """Только для модераторов каналов"""
    allowed_roles = ['channel_moderator']
    permission_denied_message = "Доступ только для модераторов каналов"

    def _test_role(self, request):
        """Дополнительная проверка статуса модератора канала"""
        return (
                super()._test_role(request) and
                hasattr(request.user, 'is_channel_moderator') and
                request.user.is_channel_moderator
        )


class StaffRequiredMixin(RoleRequiredMixin):
    """Пример добавления новой роли - персонал"""
    allowed_roles = ['staff', 'admin', 'partner']
    permission_denied_message = "Доступ только для сотрудников"

    def _get_user_role(self, request):
        """Расширяем логику определения ролей"""
        role = super()._get_user_role(request)
        if request.user.is_staff:
            return 'staff'
        if request.user.is_superuser:
            return 'admin'
        return role
