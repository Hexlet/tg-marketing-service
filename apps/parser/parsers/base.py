import logging
from telethon import TelegramClient
from apps.parser.models import TelegramChannel

log = logging.getLogger(__name__)

class BaseParser:
    """Базовый класс для всех парсеров."""

    def __init__(self, client: TelegramClient):
        self.client = client

    async def get_channel_entity(self, url: str):
        """Получить сущность канала."""
        return await self.client.get_entity(url)

    async def save_channel_model(self, channel_entity, data: dict) -> TelegramChannel:
        """Создать/обновить модель TelegramChannel."""
        channel, created = TelegramChannel.objects.get_or_create(
            telegram_id=channel_entity.id,
            defaults={
                "title": channel_entity.title,
                "username": channel_entity.username or "-",
                "is_verified": channel_entity.verified,
                "created_at": channel_entity.date,
            },
        )
        return channel
