from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class PublicationIssue(CreativeWork):
    """A part of a successively published publication such as a periodical or publication volume, often numbered, usually containing a grouping of works such as articles.\\n\\nSee also [blog post](https://blog-schema.org/2014/09/02/schema-org-support-for-bibliographic-relationships-and-periodicals/)."""
    type: str = field(default_factory=lambda: "PublicationIssue", name="@type")
    pageStart: Union[List[Union[int, str]], Union[int, str], None] = None
    pagination: Union[List[str], str, None] = None
    issueNumber: Union[List[Union[int, str]], Union[int, str], None] = None
    pageEnd: Union[List[Union[int, str]], Union[int, str], None] = None