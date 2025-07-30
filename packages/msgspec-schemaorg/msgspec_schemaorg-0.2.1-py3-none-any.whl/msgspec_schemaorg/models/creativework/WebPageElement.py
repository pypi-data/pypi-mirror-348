from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class WebPageElement(CreativeWork):
    """A web page element, like a table or an image."""
    type: str = field(default_factory=lambda: "WebPageElement", name="@type")
    xpath: Union[List[str], str, None] = None
    cssSelector: Union[List[str], str, None] = None