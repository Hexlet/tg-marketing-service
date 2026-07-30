import asyncio
import logging
from random import uniform
from typing import Dict

from telethon import TelegramClient
from telethon.errors import (
    AuthKeyError,
    ChannelInvalidError,
    FloodWaitError,
    UsernameNotOccupiedError,
)

from apps.parser.models import TelegramChannel
from apps.parser.parsers.channel import ChannelParser
from apps.parser.parsers.posts import PostsParser

log = logging.getLogger(__name__)


async def tg_parser(
    url: str,
    api_id: int,
    api_hash: str,
    limit: int = 10,
    session_name: str = "parser_session",
) -> Dict:
    """Основная функция парсинга Telegram-канала.

    Args:
        url: URL канала (например, "https://t.me/example_channel")
        api_id: ID приложения в Telegram
        api_hash: Хэш приложения в Telegram
        limit: Количество постов для парсинга
        session_name: Название сессии (по умолчанию "parser_session")

    Returns:
        Dict: Результаты парсинга, включая метаданные канала
              и статистику постов.
    """

    data = {"pinned_messages": []}

    # Инициализация клиента напрямую через TelegramClient
    client = TelegramClient(
        session_name,
        api_id,
        api_hash,
        device_model="ParserBot",
        system_version="Linux",
    )

    try:
        await client.start()
        log.info("Telegram client connected successfully")

        try:
            # Парсинг канала
            channel_parser = ChannelParser(client)
            channel_data = await channel_parser.parse_channel(url)
            data.update(channel_data)

            # Поиск модели канала в Django
            django_channel = await TelegramChannel.objects.aget(
                telegram_id=channel_data["channel_id"]
            )

            # Парсинг постов
            posts_parser = PostsParser(client)
            posts_data = await posts_parser.parse_posts(
                channel_entity=await client.get_entity(url),
                channel_model=django_channel,
                limit=limit,
            )
            data.update(posts_data)

            log.info(
                f"Successfully parsed channel {channel_data['title']} "
                f"({channel_data['username']})"
            )
            return data

        except FloodWaitError as e:
            wait_time = e.seconds + uniform(1.0, 2.0)
            log.error(f"FloodWaitError: waiting {wait_time:.1f}s")
            await asyncio.sleep(wait_time)
            raise

        except (ChannelInvalidError, UsernameNotOccupiedError):
            log.error(f"Invalid channel URL: {url}")
            raise

        except Exception as e:
            log.error(f"Unexpected error parsing {url}: {str(e)}")
            raise

    except AuthKeyError:
        log.critical("AUTH SESSION FAILURE — Telegram auth key invalid")
        raise

    finally:
        await client.disconnect()
        log.info("Telegram client disconnected")
