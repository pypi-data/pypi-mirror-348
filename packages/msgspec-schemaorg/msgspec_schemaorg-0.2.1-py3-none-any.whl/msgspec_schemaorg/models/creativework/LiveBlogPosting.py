from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.BlogPosting import BlogPosting
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.BlogPosting import BlogPosting
from datetime import datetime
from typing import Optional, Union, Dict, List, Any


class LiveBlogPosting(BlogPosting):
    """A [[LiveBlogPosting]] is a [[BlogPosting]] intended to provide a rolling textual coverage of an ongoing event through continuous updates."""
    type: str = field(default_factory=lambda: "LiveBlogPosting", name="@type")
    coverageEndTime: Union[List[datetime], datetime, None] = None
    liveBlogUpdate: Union[List['BlogPosting'], 'BlogPosting', None] = None
    coverageStartTime: Union[List[datetime], datetime, None] = None