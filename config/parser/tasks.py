import asyncio
import logging
import random
import time

from asgiref.sync import sync_to_async
from celery import shared_task
from django.conf import settings
from django.db import DatabaseError, IntegrityError
from django.utils import timezone
from telethon import TelegramClient
from telethon.sessions import StringSession

from .models import TelegramChannel, Category, Country, Language
from .parser import tg_parser

log = logging.getLogger(__name__)

def get_telegram_client():
    """Helper function to get Telegram client"""
    return TelegramClient(
        StringSession(settings.TELEGRAM_SESSION_STRING),
        settings.TELEGRAM_API_ID,
        settings.TELEGRAM_API_HASH,
    )

async def async_save_channel_data(identifier, limit=10, category_name=None, country_name=None, language_name=None):
    """Async function to parse and save channel data"""
    client = get_telegram_client()
    await client.connect()
    try:
        parsed_data = await tg_parser(identifier, client, limit)
        log.info(f'Парсинг завершен для канала; - {parsed_data.get("title")} ({parsed_data.get("channel_id")})')
        
        # Get or create related objects
        category_obj, _ = Category.objects.get_or_create(name=category_name or 'Без категории')
        country_obj, _ = Country.objects.get_or_create(name=country_name or 'Неизвестно', defaults={'code': 'XX'})
        language_obj, _ = Language.objects.get_or_create(name=language_name or 'Неизвестно')
        
        # Create or update channel
        channel, created = await TelegramChannel.objects.aupdate_or_create(
            channel_id=parsed_data["channel_id"],
            defaults={
                'title': parsed_data.get('title'),
                'username': parsed_data.get('username'),
                'description': parsed_data.get('description'),
                'subscribers_count': parsed_data.get('participants_count', 0),
                'photo_url': parsed_data.get('photo_url'),
                'avg_post_reach': parsed_data.get('average_views', 0),
                'language': language_obj,
                'country': country_obj,
                'category': category_obj,
                'parsed_at': timezone.now(),
            }
        )
        
        status = "создан" if created else "обновлен"
        log.info(f"Канал {channel.title} был успешно {status}.")
        return channel.id
    finally:
        await client.disconnect()

@shared_task
def parse_channel_task(identifier, limit=10, **kwargs):
    """Celery task to parse a single channel"""
    import asyncio
    return asyncio.run(async_save_channel_data(identifier, limit, **kwargs))

@shared_task
def parse_all_channels():
    """Celery task to parse all channels from the database"""
    import asyncio
    channel_ids = TelegramChannel.objects.values_list('channel_id', flat=True)
    for channel_id in channel_ids:
        # We can pass other stored attributes if needed
        asyncio.run(async_save_channel_data(channel_id))
