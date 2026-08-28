from datetime import datetime, timezone

from django.test import TestCase

from apps.blog.dto.blog_dto import ArticleCardDTO, BlogListDTO
from apps.blog.models import BlogArticle
from apps.blog.services.blog_list_service import BlogListService


class BlogListServiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.featured = BlogArticle.objects.create(
            title="Главная статья",
            slug="glavnaya-statya",
            excerpt="Анонс главной статьи.",
            is_featured=True,
            is_published=True,
            published_at=datetime(2026, 8, 4, 8, 0, tzinfo=timezone.utc),
        )

        cls.featured_older = BlogArticle.objects.create(
            title="Старая featured",
            slug="staraya-featured",
            excerpt="Тоже в избранном, но опубликована раньше.",
            is_featured=True,
            is_published=True,
            published_at=datetime(2026, 7, 20, 10, 0, tzinfo=timezone.utc),
        )

        cls.article = BlogArticle.objects.create(
            title="Обычная статья",
            slug="obychnaya-statya",
            excerpt="Анонс обычной статьи.",
            is_featured=False,
            is_published=True,
            published_at=datetime(2026, 7, 10, 9, 0, tzinfo=timezone.utc),
        )

        cls.unpublished = BlogArticle.objects.create(
            title="Черновик",
            slug="chernovik",
            excerpt="Ещё не опубликовано.",
            is_featured=False,
            is_published=False,
        )

    def test_build_returns_blog_list_dto(self) -> None:
        dto = BlogListService().build()

        self.assertIsInstance(dto, BlogListDTO)
        self.assertIsInstance(dto.featured, ArticleCardDTO)
        self.assertTrue(
            all(isinstance(article, ArticleCardDTO) for article in dto.articles)
        )

        self.assertEqual(dto.featured.slug, self.featured.slug)

        articles_slugs = [article.slug for article in dto.articles]
        self.assertEqual(
            articles_slugs, [self.featured_older.slug, self.article.slug]
        )
        self.assertNotIn(self.unpublished.slug, articles_slugs)
