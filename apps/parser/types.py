from typing import TypedDict


class ParsedMessage(TypedDict):
    post_id: int
    post_text: str | None
    post_views: int | None


class PinnedMessage(TypedDict):
    text: str
    id: int | None


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
