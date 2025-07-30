from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class WebSite(CreativeWork):
    """A WebSite is a set of related web pages and other items typically served from a single web domain and accessible via URLs."""
    type: str = field(default_factory=lambda: "WebSite", name="@type")
    issn: Union[List[str], str, None] = None