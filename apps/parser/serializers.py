from django.contrib import admin
from django.db.models import Sum

from apps.parser.models import Post


class PostSerializer:
    """
    Сериализатор для модели Post и связанных метрик.
    Предназначен для передачи данных в Inertia через props.
    """

    @classmethod
    def get_post_data(cls, post: Post) -> dict:
        reactions = (
            post.reactions.values("emoji")
            .annotate(count=Sum("count"))
            .order_by("-count")
        )

        reaction_details_dict = {}
        total_reactions = 0

        for item in reactions:
            emoji = item["emoji"]
            count = item["count"]
            reaction_details_dict[emoji] = count
            total_reactions += count

        return {
            "id": post.id,
            "telegram_message_id": post.telegram_message_id,
            "channel_id": post.channel.id,
            "text": post.text,
            "published_at": post.published_at.isoformat(),
            "views": post.views,
            "forwards": post.forwards,
            "comments_count": post.comments_count,
            "reposts": post.reposts,
            "is_pinned": post.is_pinned,
            "media_type": post.media_type,
            "permalink": post.permalink,
            "reactions": {
                "total": total_reactions,
                "details": reaction_details_dict,
            },
        }

    @classmethod
    def get_posts_list_data(cls, queryset) -> list[dict]:
        """
        Возвращает список сериализованных постов для представления списка
        """
        return [cls.get_post_data(post) for post in queryset]

    @staticmethod
    def get_admin_list_display() -> list:
        """
        Ключевые метрики для отображения в админке (list_display)
        """
        return [
            "telegram_message_id",
            "text_preview",
            "published_at",
            "views",
            "forwards",
            "comments_count",
            "reposts",
            "is_pinned",
            "media_type",
            "permalink",
            "total_reactions",
        ]

    @classmethod
    def get_admin_list_filter(cls) -> tuple:
        """
        Поля для фильтрации в админке
        """
        return (
            "media_type",
            "is_pinned",
            "published_at",
            ("channel", admin.RelatedFieldListFilter),
        )

    @classmethod
    def get_admin_search_fields(cls) -> tuple:
        """
        Поля для поиска в админке
        """
        return (
            "telegram_message_id",
            "text",
            "channel__title",
            "channel__username",
        )

    @classmethod
    def get_serialized_post_for_inertia(cls, post_id: int) -> dict:
        """
        Получает пост по ID и возвращает его в формате, пригодном для Inertia

        """
        try:
            post = Post.objects.get(id=post_id)
            return cls.get_post_data(post)
        except Post.DoesNotExist:
            raise Post.DoesNotExist(f"Post with id {post_id} does not exist")
