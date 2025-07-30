from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.BlogPosting import BlogPosting
from typing import Optional, Union, Dict, List, Any


class Blog(CreativeWork):
    """A [blog](https://en.wikipedia.org/wiki/Blog), sometimes known as a "weblog". Note that the individual posts ([[BlogPosting]]s) in a [[Blog]] are often colloquially referred to by the same term."""
    type: str = field(default_factory=lambda: "Blog", name="@type")
    blogPost: Union[List['BlogPosting'], 'BlogPosting', None] = None
    blogPosts: Union[List['BlogPosting'], 'BlogPosting', None] = None
    issn: Union[List[str], str, None] = None