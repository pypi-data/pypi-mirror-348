from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class Chapter(CreativeWork):
    """One of the sections into which a book is divided. A chapter usually has a section number or a name."""
    type: str = field(default_factory=lambda: "Chapter", name="@type")
    pageStart: Union[List[Union[int, str]], Union[int, str], None] = None
    pagination: Union[List[str], str, None] = None
    pageEnd: Union[List[Union[int, str]], Union[int, str], None] = None