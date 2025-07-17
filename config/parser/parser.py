import asyncio
import time
import random
from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.errors import (
    FloodWaitError,
    UsernameNotOccupiedError,
    ChannelInvalidError,
    AuthKeyError,
    ForbiddenError,
)

import logging

log = logging.getLogger(__name__)


async def tg_parser(url: str, client: TelegramClient, limit: int = 10) -> dict:
    """
    Функция-парсер телеграм каналов, позволяет получить данные о телеграм канале,
    включая: название, id, описание, количество подписчиков, закрепленное сообщение, последние посты.
    Параметры:
    url (str): ссылка на телеграм канал в любом из удобных видов (https://t.me/example, t.me/example, @example, example)
    client (TelegramClient): клиент телеграма из библиотеки telethon
    limit (int): количество сообщений для парсинга, по умолчанию 10
    Возвращаемое значение:
    data (dict): словарь с данными телеграм канала
    Примечание:
    Для работы данной функции необходима регистрация приложения telegram API
    """
    data = {}
    full_channel = None
    pinned_messages = None

    try:
        # антифлуд, убрать когда будет выделенный номер
        time.sleep(1)
        # получаем информацию о канале
        channel = await client.get_entity(url)
        data['title'] = channel.title # название канала
        data['channel_id'] = channel.id # id канала
        data['username'] = channel.username # юзернейм канала
        data['verified'] = channel.verified # верифицирован ли канал (булево)
        # дата создания канала
        data['creation_date'] = channel.date.isoformat() if channel.date else None
        # получаем 10 последних постов из канала
        last_messages = await client.get_messages(channel, limit=limit * 3)
        # получаем среднее количество просмотров последних постов
        data['last_messages'] = [{'post_id': post.id, 'post_text': post.text, 'post_views': post.views}
                                        for post in last_messages[:limit]]
        total_views = 0
        total_posts = 0
        for post in last_messages:
            total_views += post.views
            total_posts += 1
        average_views = total_views // total_posts
        data['average_views'] = average_views

    except FloodWaitError as e:
        log.error(f'Сработал антифлуд, нужно подождать')
        # ждем рекомендуемое время + случайный промежуток
        await asyncio.sleep(e.seconds + random.uniform(1.0, 2.0))

    except ChannelInvalidError:
        log.warning(f'Канал приватный или недоступен: {url}')

    except UsernameNotOccupiedError:
        log.error(f'Несуществующий юзернейм: {url}')

    except AuthKeyError:
        log.critical(f'Проблемы с сессией авторизации')

    if channel:

        try:
            # получаем полную информацию о канале
            full_channel = await client(GetFullChannelRequest(channel))

        except FloodWaitError as e:
            log.error(f'Сработал антифлуд, нужно подождать')
            # ждем рекомендуемое время + случайный промежуток
            await asyncio.sleep(e.seconds + random.uniform(1.0, 2.0))

        except ForbiddenError:
            log.warning(f'Ошибка доступа к полной информации канала')

        if full_channel:
            # получаем количество участников
            participants_count = full_channel.full_chat.participants_count
            data['participants_count'] = participants_count if participants_count else 'Нет участников'
            # получаем описание канала
            description = full_channel.full_chat.about
            data['description'] = description if description else 'Нет описания'
            # получаем id закрепленного сообщения
            pinned_message_id = full_channel.full_chat.pinned_msg_id
            # получаем закрепленное сообщение
            if pinned_message_id:
                pinned_messages = await client.get_messages(channel, ids=pinned_message_id)
            data['pinned_messages'] = [{
                'text': pinned_messages.message if pinned_messages else 'Нет закрепленного сообщения',
                'id': pinned_message_id if pinned_messages else None
                }]

    log.debug(f'Канал успешно спарсился: {data}')
    return data