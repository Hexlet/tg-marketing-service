from django.views.generic.base import View
from inertia import render as inertia_render
from apps.homepage.models import HomePageComponent


class IndexView(View):
    def get(self, request, *args, **kwargs):
        components = HomePageComponent.objects.filter(is_active=True).order_by('order')
        page_data = {
            'components': [
                {
                    'id': component.id,
                    'type': component.component_type,
                    'title': component.title,
                    'content': component.content,
                    'order': component.order
                }
                for component in components
            ],
        }

        return inertia_render(request, 'Home', props=page_data)
