from django.views.generic.base import View
from inertia import render as inertia_render
from apps.homepage.models import HomePageComponent
from django.http import HttpRequest, HttpResponse

class IndexView(View):
    """
    Главная страница сайта.

    Документация компонентов для InertiaJS:
    [
        {
            "component": "HomePageComponent",
            "props": ["id", "type", "title", "content", "order"],
            "url": "/"
        }
    ]
    """

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        # Получаем все активные компоненты, сортируем по порядку
        components = (
            HomePageComponent.objects
            .filter(is_active=True)
            .order_by('order')
        )

        # Формируем props для Inertia
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

        # Возвращаем Inertia Response с шаблоном 'Home' и данными компонентов
        return inertia_render(request, 'Home', props=page_data)

