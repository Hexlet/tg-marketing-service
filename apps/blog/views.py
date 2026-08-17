from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views import View

from apps.blog.services.blog_list_service import BlogListService
from config.renderers import render_inertia_from_dto


class BlogListView(View):
    """
    Inertia view для публичного списка блога (/blog/).

    Пример Inertia payload для фронтенда (значения пока иллюстративные):

    {
        "component": "Blog",
        "props": {
            "featured": {
                "id": 1,
                "slug": "podborka-plaginov-dlya-vs-code-selectel",
                "title": "Подборка плагинов для VS Code",
                "excerpt": "Какие расширения реально экономят часы рутины.",
                "cover_image": "https://example.com/cover.jpg",
                "category": "dev",
                "tags": ["vs code", "плагины"],
                "read_time": 12,
                "published_at": "2026-08-04T08:00:00+00:00",
                "views_count": 120,
                "author_name": "Иван Иванов"
            },
            "articles": [
                {
                    "id": 2,
                    "slug": "sut-asinhronnosti-v-python",
                    "title": "Суть асинхронности в Python",
                    "excerpt": "Корутины, событийный цикл и таски без магии.",
                    "cover_image": "https://example.com/cover2.jpg",
                    "category": "dev",
                    "tags": ["python", "asyncio"],
                    "read_time": 8,
                    "published_at": "2026-07-05T14:00:00+00:00",
                    "views_count": 89,
                    "author_name": "Иван Иванов"
                }
            ]
        },
        "url": "/blog/"
    }

    Примечания:
    - отдаются только опубликованные статьи (is_published=True);
    - featured: последняя статья с is_featured=True, может отсутствовать
      (тогда фронт получает null и не рисует выделенный блок);
    - articles: остальные опубликованные статьи без featured,
      упорядоченные по published_at desc;
    - страница публичная, авторизация не требуется.
    """

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        dto = BlogListService().build()
        return render_inertia_from_dto(request, "Blog", props=dto)
