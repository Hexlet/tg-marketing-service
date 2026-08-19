from collections.abc import Mapping
from typing import Any, TypedDict


class ParsedMessage(TypedDict):
    post_id: int
    post_text: str | None
    post_views: int | None


class PinnedMessage(TypedDict):
    text: str
    id: int | None


class ParsedPostsData(TypedDict, total=False):
    total_posts: int
    average_views: int
    average_comments: int
    average_reposts: int


class ParsedChannelData(TypedDict):
    title: str
    channel_id: int
    username: str | None
    verified: bool | None
    creation_date: str | None
    last_messages: list[ParsedMessage]
    average_views: int
    participants_count: int
    description: str
    pinned_messages: list[PinnedMessage]


class ParsedChannelResult(TypedDict, total=False):
    title: str
    channel_id: int
    username: str | None
    verified: bool | None
    creation_date: str | None
    last_messages: list[ParsedMessage]
    participants_count: int
    description: str
    pinned_messages: list[PinnedMessage]
    average_views: int
    total_posts: int
    average_comments: int
    average_reposts: int


class PartialParsedChannelData(TypedDict, total=False):
    title: str
    channel_id: int
    username: str | None
    verified: bool | None
    creation_date: str | None
    last_messages: list[ParsedMessage]
    average_views: int
    participants_count: int
    description: str
    pinned_messages: list[PinnedMessage]


class ChannelDataForSave(ParsedChannelData, total=False):
    language: str
    country: str
    category: str


def normalize_channel_data(data: Mapping[str, Any]) -> ParsedChannelData:
    return {
        "title": data["title"],
        "channel_id": data["channel_id"],
        "username": data.get("username"),
        "verified": data.get("verified"),
        "creation_date": data.get("creation_date"),
        "last_messages": data.get("last_messages", []),
        "average_views": data.get("average_views", 0),
        "participants_count": data.get("participants_count", 0),
        "description": data.get("description", "Нет описания"),
        "pinned_messages": data.get("pinned_messages", []),
    }


def build_parsed_channel_result(
    data: Mapping[str, Any],
) -> ParsedChannelResult:
    return {
        "title": data["title"],
        "channel_id": data["channel_id"],
        "username": data.get("username"),
        "verified": data.get("verified"),
        "creation_date": data.get("creation_date"),
        "last_messages": data.get("last_messages", []),
        "average_views": data.get("average_views", 0),
        "participants_count": data.get("participants_count", 0),
        "description": data.get("description", "Нет описания"),
        "pinned_messages": data.get("pinned_messages", []),
        "total_posts": data.get("total_posts", 0),
        "average_comments": data.get("average_comments", 0),
        "average_reposts": data.get("average_reposts", 0),
    }
