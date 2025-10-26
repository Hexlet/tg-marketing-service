from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.contrib import messages


class RoleRequiredMixin(AccessMixin):
    """
    Базовый миксин для проверки ролей.
    Наследуем от AccessMixin для стандартного поведения Django.
    """
    allowed_roles = None  # Обязательно переопределить в дочерних классах
    permission_denied_message = "У вас нет прав для доступа к этой странице"
    redirect_url = '/'  # URL для перенаправления при отказе в доступе

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
            return self.redirect_to_login()  # Перенаправляем гостей на страницу входа
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.redirect_url)


class GuestRequiredMixin(RoleRequiredMixin):
    """Только для неавторизованных пользователей"""
    allowed_roles = ['guest']
    permission_denied_message = "Эта страница доступна только гостям"
    redirect_url = '/'


class UserRequiredMixin(RoleRequiredMixin):
    """Для всех авторизованных пользователей"""
    allowed_roles = ['user', 'partner', 'channel_moderator']
    permission_denied_message = "Требуется авторизация"
    redirect_url = '/'


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
