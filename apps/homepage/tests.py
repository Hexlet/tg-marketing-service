import json
from django.test import TestCase
from django.urls import reverse
from apps.homepage.models import HomePageComponent
from django.test import RequestFactory
from apps.homepage.views import IndexView


class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.component = HomePageComponent.objects.create(
            title="My Component Title",
            content="Some content here",
            order=1,
            is_active=True
        )

    def test_index_view_with_inertia_props(self):
        # Выполняем запрос к нашему view
        factory = RequestFactory()
        request = factory.get(reverse('main_index'), HTTP_ACCEPT='application/json')
        response = IndexView.as_view()(request)
        
        try:
            # Попытка преобразования ответа в JSON
            data = json.loads(response.content.decode())
        except Exception as e:
            self.fail(f"Failed to parse JSON: {e}, Content Type: {response.headers.get('Content-Type')}")
            raise

        # Остальные проверки оставлены такими же
        self.assertIn('props', data)
        self.assertIsInstance(data['props'], dict)

        self.assertIn('components', data['props'])
        components = data['props']['components']

        self.assertGreater(len(components), 0)
        first_component = components[0]
        self.assertEqual(first_component['title'], self.component.title)
        self.assertEqual(first_component['content'], self.component.content)
        self.assertEqual(first_component['order'], self.component.order)
