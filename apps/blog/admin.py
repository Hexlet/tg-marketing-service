from django.contrib import admin
from guardian.admin import GuardedModelAdminMixin

from apps.blog.models import BlogArticle


@admin.register(BlogArticle)
class BlogArticleAdmin(GuardedModelAdminMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "is_featured",
        "is_published",
        "published_at",
        "read_time",
        "views_count",
    )
    list_editable = ("is_featured", "is_published")
    list_filter = ("is_published", "is_featured", "category")
    search_fields = ("title", "slug", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering = ("-published_at", "-created_at")
    list_select_related = ("author",)

    fieldsets = (
        (
            "Основная информация",
            {"fields": ("title", "slug", "author", "category", "tags")},
        ),
        (
            "Содержимое",
            {
                "fields": ("excerpt", "cover_image", "body"),
                "description": "Текст статьи в формате Markdown.",
            },
        ),
        (
            "Публикация",
            {
                "fields": (
                    "is_featured",
                    "is_published",
                    "published_at",
                    "read_time",
                    "views_count",
                ),
            },
        ),
    )
