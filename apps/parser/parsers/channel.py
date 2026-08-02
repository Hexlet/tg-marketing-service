import logging
from typing import Dict

from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import Channel

from apps.parser.parsers.base import BaseParser

log = logging.getLogger(__name__)


class ChannelParser(BaseParser):
    """Парсер метаданных Telegram-канала."""

    async def parse_channel(self, url: str) -> Dict:
        """Парсинг информации о канале."""
        channel_entity: Channel = await self.get_channel_entity(url)
        data = {
            "title": channel_entity.title,
            "channel_id": channel_entity.id,
            "username": channel_entity.username or "-",
            "verified": channel_entity.verified,
            "creation_date": (
                channel_entity.date.isoformat() if channel_entity.date else None
            ),
        }

        # Сохранение модели канала
        django_channel = await self.save_channel_model(channel_entity, data)

        # Получение полной информации о канале
        # (участники, описание, закреплённое сообщение)
        try:
            full_channel = await self.client(
                GetFullChannelRequest(channel=channel_entity)
            )
            data.update(
                {
                    "participants_count": (
                        full_channel.full_chat.participants_count or 0
                    ),
                    "description": (
                        full_channel.full_chat.about or "Нет описания"
                    ),
                }
            )
            django_channel.description = data["description"]
            django_channel.subscribers_count = data["participants_count"]
            await django_channel.asave(
                update_fields=["description", "subscribers_count"]
            )

            # Обработка закреплённого сообщения
            pinned_msg_id = full_channel.full_chat.pinned_msg_id
            if pinned_msg_id:
                pinned_message = await self.client.get_messages(
                    channel_entity, ids=pinned_msg_id
                )
                data["pinned_messages"] = [
                    {
                        "text": pinned_message.text or "Нет текста",
                        "id": pinned_message.id,
                        "date": (
                            pinned_message.date.isoformat()
                            if pinned_message.date
                            else None
                        ),
                    }
                ]
        except Exception as e:
            log.error(f"Error fetching full channel info: {e}")
            data["description"] = "Нет описания (ошибка)"

        return data
