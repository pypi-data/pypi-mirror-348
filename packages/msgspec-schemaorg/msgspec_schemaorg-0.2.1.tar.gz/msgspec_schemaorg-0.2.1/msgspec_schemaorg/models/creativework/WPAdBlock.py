from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.WebPageElement import WebPageElement
from typing import Optional, Union, Dict, List, Any


class WPAdBlock(WebPageElement):
    """An advertising section of the page."""
    type: str = field(default_factory=lambda: "WPAdBlock", name="@type")