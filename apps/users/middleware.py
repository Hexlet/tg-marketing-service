from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            request.role = 'guest'
        else:
            try:
                if hasattr(request.user, 'partner_profile') and request.user.partner_profile.status == 'active':
                    request.role = 'partner'
                elif hasattr(request.user, 'is_channel_moderator') and request.user.is_channel_moderator:
                    request.role = 'channel_moderator'
                else:
                    request.role = 'user'
            except ObjectDoesNotExist:
                request.role = 'user'

        response = self.get_response(request)
        return response