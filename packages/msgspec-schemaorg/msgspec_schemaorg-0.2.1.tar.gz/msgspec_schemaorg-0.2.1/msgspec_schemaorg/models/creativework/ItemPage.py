from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.WebPage import WebPage
from typing import Optional, Union, Dict, List, Any


class ItemPage(WebPage):
    """A page devoted to a single item, such as a particular product or hotel."""
    type: str = field(default_factory=lambda: "ItemPage", name="@type")