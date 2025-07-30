from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.WebPage import WebPage
from typing import Optional, Union, Dict, List, Any


class CollectionPage(WebPage):
    """Web page type: Collection page."""
    type: str = field(default_factory=lambda: "CollectionPage", name="@type")