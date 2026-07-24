from typing import List, Dict
from telethon import TelegramClient
from telethon.tl.types import Message, Channel
from apps.parser.models import TelegramChannel, Post, PostReaction


class PostsParser:
    """Парсер постов и реакций."""

    def __init__(self, client: TelegramClient):
        self.client = client

    async def parse_posts(
        self,
        channel_entity: 'Channel',
        channel_model: TelegramChannel,
        limit: int = 10,
    ) -> Dict:
        """Парсинг постов и реакций."""
        last_messages: List[Message] = await self.client.get_messages(channel_entity, limit=limit * 3)
        total_views = 0
        total_comments = 0
        total_reposts = 0
        post_count = 0

        for message in last_messages[:limit]:
            if message.service:
                continue

            # Обработка поста
            post, created = await Post.objects.aget_or_create(
                channel=channel_model,
                telegram_message_id=message.id,
                defaults={
                    "text": message.text or "",
                    "published_at": message.date,
                    "views": message.views or 0,
                    "permalink": f"https://t.me/{channel_entity.username}/{message.id}" if channel_entity.username else None,
                },
            )

            # Обновление просмотров (если уже существует)
            if not created and message.views:
                post.views = max(post.views, message.views)
                post.save(update_fields=["views"])

            # Обработка реакций
            if message.reactions:
                for reaction in message.reactions.results:
                    await PostReaction.objects.aupdate_or_create(
                        post=post,
                        emoji=reaction.reaction,
                        defaults={"count": reaction.count},
                    )

            # Сбор статистики
            if message.views:
                total_views += message.views
            if message.replies and message.replies.replies:
                total_comments += message.replies.replies
            if message.forwards:
                total_reposts += message.forwards
            post_count += 1

        return {
            "total_posts": post_count,
            "average_views": total_views // max(post_count, 1),
            "average_comments": total_comments // max(post_count, 1),
            "average_reposts": total_reposts // max(post_count, 1),
        }
