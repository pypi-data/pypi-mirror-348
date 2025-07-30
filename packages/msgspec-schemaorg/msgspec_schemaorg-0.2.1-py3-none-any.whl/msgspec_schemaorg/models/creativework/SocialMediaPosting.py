from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Article import Article
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class SocialMediaPosting(Article):
    """A post to a social media platform, including blog posts, tweets, Facebook posts, etc."""
    type: str = field(default_factory=lambda: "SocialMediaPosting", name="@type")
    sharedContent: Union[List['CreativeWork'], 'CreativeWork', None] = None