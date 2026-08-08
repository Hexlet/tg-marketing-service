import asyncio
import logging
import random
import time
from typing import Any

from telethon import TelegramClient
from telethon.errors import (
    AuthKeyError,
    ChannelInvalidError,
    FloodWaitError,
    ForbiddenError,
    UsernameNotOccupiedError,
)
from telethon.tl.functions.channels import GetFullChannelRequest

from apps.parser.types import ParsedChannelData, PartialParsedChannelData

log = logging.getLogger(__name__)


async def tg_parser(
    url: str | int, client: TelegramClient, limit: int = 10
) -> ParsedChannelData | None:
    """
    Telegram channel parser function. Retrieves channel data including:
    name, ID, description, subscriber count, pinned message, and recent posts.

    Parameters:
        url (str | int): URL, username, or numeric ID of the Telegram channel
                         in any valid format (e.g., `https://t.me/example`,
                         `t.me/example`, `@example`, `example`)
        client (TelegramClient): A Telegram client instance from the
                                 `telethon` library
        limit (int): Number of messages to parse (default: 10)

    Returns:
        data (dict): A dictionary containing the parsed Telegram channel data

    Note:
        This function requires a registered Telegram API application to work.
    """
    data: PartialParsedChannelData = {}
    channel: Any | None = None
    full_channel: Any | None = None
    pinned_message: Any | None = None

    try:
        # Anti-flood - remove when dedicated number is assigned
        time.sleep(1)
        # Gets channel information
        channel = await client.get_entity(url)

        data["title"] = channel.title  # Channel title
        data["channel_id"] = channel.id  # Channel id
        data["username"] = channel.username  # Channel username
        data["verified"] = channel.verified  # Is channel verified? (boolean)
        # Channel creation date
        data["creation_date"] = (
            channel.date.isoformat() if channel.date else None
        )
        # Fetches last channel posts

        last_messages = await client.get_messages(channel, limit=limit * 3)
        # Calculates average views of recent posts
        data["last_messages"] = [
            {
                "post_id": post.id,
                "post_text": post.text,
                "post_views": post.views,
            }
            for post in last_messages[:limit]
        ]
        total_views = 0
        total_posts = 0

        for post in last_messages:
            if post.views:
                total_views += post.views
                total_posts += 1
        average_views = total_views // total_posts if total_posts else 0
        data["average_views"] = average_views

    except FloodWaitError as e:
        log.error("Anti-flood triggered, waiting required")
        # wait recommended time + random interval

        await asyncio.sleep(e.seconds + random.uniform(1.0, 2.0))
        return None

    except ChannelInvalidError:
        log.warning(f"This channel is private or unavailable: {url}")
        return None

    except UsernameNotOccupiedError:
        log.error(f"Username does not exist: {url}")
        return None

    except AuthKeyError:
        log.critical("AUTH SESSION FAILURE")
        return None

    except Exception as e:
        log.error(f"ERROR - {e}")
        return None

    if channel:
        try:
            # Fetch complete channel information
            full_channel = await client(GetFullChannelRequest(channel))

        except FloodWaitError as e:
            log.error("Anti-flood triggered, waiting required")
            # wait recommended time + random interval
            await asyncio.sleep(e.seconds + random.uniform(1.0, 2.0))

        except ForbiddenError:
            log.warning("Failed to access full channel information")

        except Exception as e:
            log.error(f"ERROR - {e}")

        if full_channel:
            # Fetching channel participants count
            participants_count = full_channel.full_chat.participants_count
            data["participants_count"] = participants_count or 0
            # Fetching channel description
            description = full_channel.full_chat.about
            data["description"] = description if description else "Нет описания"
            # Fetchin pinned message id
            pinned_message_id = full_channel.full_chat.pinned_msg_id
            # Fetching pinned message
            if pinned_message_id:
                try:
                    pinned_message = await client.get_messages(
                        channel, ids=pinned_message_id
                    )
                except Exception as e:
                    log.error(f"Failed to fetch pinned message: {e}")
            data["pinned_messages"] = [
                {
                    "text": (pinned_message.message or "")
                    if pinned_message
                    else "Нет закрепленного сообщения",
                    "id": pinned_message_id if pinned_message else None,
                }
            ]

    if channel is None:
        return None

    parsed_data = ParsedChannelData(
        title=data["title"],
        channel_id=data["channel_id"],
        username=data["username"],
        verified=data["verified"],
        creation_date=data["creation_date"],
        last_messages=data["last_messages"],
        average_views=data["average_views"],
        participants_count=data.get("participants_count", 0),
        description=data.get("description", "Нет описания"),
        pinned_messages=data.get("pinned_messages", []),
    )

    log.debug(f"Channel successfully parsed: {parsed_data}")
    return parsed_data
