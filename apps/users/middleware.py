from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from config import settings

User = get_user_model()


class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        roles_map = dict(settings.USER_ROLES)
    
        # Получаем роль пользователя, если она известна
        user_role = getattr(request.user, 'role', None)
        
        # Если роль пользователя не найдена, ставим гостевую роль
        final_role = roles_map[user_role] if user_role else roles_map['guest']
    
        # Ставим роль в запрос
        request.role = final_role
    
        response = self.get_response(request)
        print(f"Middleware: Current role of the user is '{request.role}'")
        return response