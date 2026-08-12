from django.contrib import admin

from apps.parser.models import Post


class PostSerializer:
    """
    Сериализатор для модели Post и связанных метрик.
    Предназначен для передачи данных в Inertia через props.
    """

    @classmethod
    def get_post_data(cls, post: Post) -> dict:
        breakdown = post.get_reactions_breakdown()

        ai_data = {}

        """
        Словарь пропсов для фронтенда (Inertia.js).
        Формат соответствует требованиям UI:
        - summary: краткое описание
        - sentiment: тон
        - why_visited: (извлекается из audience_insight или summary)
        - improvements: (из recommendations)
        - similar_ideas: (из key_topics или доп. поля)
        """

        if hasattr(post, "ai_breakdown"):
            ai = post.ai_breakdown
            ai_data = {
                "summary": ai.summary,
                "sentiment": ai.sentiment,
                "key_topics": ai.key_topics,
                "audience_insight": ai.audience_insight,
                "recommendations": ai.recommendations,
                "generated_at": ai.generated_at.isoformat(),
                "model_version": ai.model_version,
            }

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
                "total": breakdown["total"],
                "details": breakdown["details"],
            },
            "ai_breakdown": ai_data,
        }

    @classmethod
    def get_serialized_post_for_inertia(cls, post_id: int) -> dict:
        try:
            # select_related, чтобы подтянуть AI данные одним запросом
            post = Post.objects.select_related("ai_breakdown").get(id=post_id)
            return cls.get_post_data(post)
        except Post.DoesNotExist:
            raise Post.DoesNotExist(f"Post with id {post_id} does not exist")

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
