from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Comment import Comment
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class Comment(CreativeWork):
    """A comment on an item - for example, a comment on a blog post. The comment's content is expressed via the [[text]] property, and its topic via [[about]], properties shared with all CreativeWorks."""
    type: str = field(default_factory=lambda: "Comment", name="@type")
    parentItem: Union[List[Union['Comment', 'CreativeWork']], Union['Comment', 'CreativeWork'], None] = None
    upvoteCount: Union[List[int], int, None] = None
    downvoteCount: Union[List[int], int, None] = None
    sharedContent: Union[List['CreativeWork'], 'CreativeWork', None] = None