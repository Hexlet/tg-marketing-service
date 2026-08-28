from typing import Optional

from django.db.models import QuerySet

from apps.blog.dto.blog_dto import ArticleCardDTO, BlogListDTO
from apps.blog.models import BlogArticle


class BlogListService:
    """
    Собирает данные для страницы списка блога (Inertia 'Blog', /blog/).

    Возвращает:
    - featured: последняя опубликованная статья с is_featured=True;
    - articles: все остальные опубликованные статьи (без featured),
      отсортированные по published_at desc.
    """

    def build(self) -> BlogListDTO:
        featured = self._get_featured_article()
        articles_qs = self._get_articles_queryset(featured)

        return BlogListDTO(
            featured=self._to_card(featured) if featured else None,
            articles=[self._to_card(article) for article in articles_qs],
        )

    # ------------------------
    # QuerySets
    # ------------------------

    def _get_featured_article(self) -> Optional[BlogArticle]:
        return (
            BlogArticle.objects.filter(is_published=True, is_featured=True)
            .order_by("-published_at", "-created_at")
            .select_related("author")
            .first()
        )

    def _get_articles_queryset(
        self, featured: Optional[BlogArticle]
    ) -> QuerySet[BlogArticle]:
        qs = BlogArticle.objects.filter(is_published=True).select_related(
            "author"
        )
        if featured is not None:
            qs = qs.exclude(pk=featured.pk)
        return qs.order_by("-published_at", "-created_at")

    # ------------------------
    # Mappers
    # ------------------------

    def _to_card(self, article: BlogArticle) -> ArticleCardDTO:
        return ArticleCardDTO(
            id=article.id,
            slug=article.slug,
            title=article.title,
            excerpt=article.excerpt,
            cover_image=article.cover_image,
            category=article.category,
            tags=list(article.tags or []),
            read_time=article.read_time,
            published_at=article.published_at,
            views_count=article.views_count,
            author_name=self._get_author_name(article),
        )

    def _get_author_name(self, article: BlogArticle) -> Optional[str]:
        author = article.author
        if author is None:
            return None
        return author.get_full_name() or author.username
