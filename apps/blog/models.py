from django.conf import settings
from django.db import models


class BlogArticle(models.Model):
    CATEGORY_CHOICES = [
        ("marketing", "Маркетинг"),
        ("telegram", "Telegram"),
        ("ai", "ИИ и автоматизация"),
        ("product", "Продукт"),
        ("dev", "Разработка"),
        ("news", "Новости"),
    ]

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(
        max_length=220,
        unique=True,
        verbose_name="Слаг",
        help_text="Используется в URL статьи.",
    )
    excerpt = models.TextField(
        verbose_name="Анонс",
        help_text="Краткое описание для карточки статьи.",
    )
    cover_image = models.URLField(
        verbose_name="Обложка",
        blank=True,
        help_text="URL изображения обложки.",
    )
    body = models.TextField(
        verbose_name="Текст статьи",
        help_text="Markdown или rich text.",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_articles",
        verbose_name="Автор",
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="marketing",
        verbose_name="Категория",
    )
    tags = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Теги",
        help_text="Список строк-тегов.",
    )
    is_featured = models.BooleanField(default=False, verbose_name="В избранном")
    is_published = models.BooleanField(
        default=False, verbose_name="Опубликована"
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата публикации",
    )
    read_time = models.PositiveIntegerField(
        default=5,
        verbose_name="Время чтения (мин)",
    )
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Просмотры",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлена")

    class Meta:
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога"
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["is_published", "is_featured"]),
        ]

    def __str__(self):
        return self.title
