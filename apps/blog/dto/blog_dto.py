from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ArticleCardDTO(BaseModel):
    """Карточка статьи для списка блога."""

    id: int
    slug: str
    title: str
    excerpt: str
    cover_image: str = ""
    category: str
    tags: List[str] = Field(default_factory=list)
    read_time: int = Field(ge=0)
    published_at: Optional[datetime] = None
    views_count: int = Field(ge=0)
    author_name: Optional[str] = None


class BlogListDTO(BaseModel):
    """Props для Inertia-страницы 'Blog' (/blog/).

    - featured: выделенная статья (последняя is_featured & is_published);
    - articles: остальные статьи, упорядоченные по published_at desc.
    """

    featured: Optional[ArticleCardDTO] = None
    articles: List[ArticleCardDTO]
