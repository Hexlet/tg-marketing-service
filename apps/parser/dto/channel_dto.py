from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ChannelDTO(BaseModel):
    id: int
    username: Optional[str]
    title: str
    description: Optional[str]
    participants_count: int = Field(ge=0)
    parsed_at: Optional[datetime]
    pinned_messages: List[dict] = Field(default_factory=list)
    creation_date: Optional[datetime]
    last_messages: List[dict] = Field(default_factory=list)
    average_views: int = 0
    category: Optional[str]
    country: Optional[str]
    language: Optional[str]


class ChannelListDTO(BaseModel):
    channels: List[ChannelDTO]
