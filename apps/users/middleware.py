import logging
from collections.abc import Callable
from typing import cast

from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse

from apps.users.roles import Role

logger = logging.getLogger(__name__)
User = get_user_model()


class RoleRequest(HttpRequest):
    role: str


class RoleMiddleware:
    def __init__(
        self,
        get_response: Callable[[HttpRequest], HttpResponse],
    ) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Получаем роль пользователя, если она известна
        user_role = getattr(request.user, "role", None)
        role_obj = Role._default_manager.filter(code=user_role).first()

        # Если роль пользователя не найдена, ставим гостевую роль
        if role_obj:
            final_role = role_obj.code
        elif user_role:
            final_role = user_role
        else:
            final_role = "guest"

        # Ставим роль в запрос
        cast(RoleRequest, request).role = final_role

        logger.debug(
            "Middleware: Current role of the user is '%s'", request.role
        )

        response = self.get_response(request)

        return response
