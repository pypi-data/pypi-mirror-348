from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.WebPage import WebPage
from typing import Optional, Union, Dict, List, Any


class ProfilePage(WebPage):
    """Web page type: Profile page."""
    type: str = field(default_factory=lambda: "ProfilePage", name="@type")