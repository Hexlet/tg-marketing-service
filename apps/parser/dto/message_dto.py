from typing import Optional

from pydantic import BaseModel


class PinnedMessageDTO(BaseModel):
    text: str
    id: Optional[int] = None


class LastMessageDTO(BaseModel):
    post_id: int
    post_text: Optional[str] = None
    post_views: Optional[int] = None
