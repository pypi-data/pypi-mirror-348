from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CollectionPage import CollectionPage
from typing import Optional, Union, Dict, List, Any


class MediaGallery(CollectionPage):
    """Web page type: Media gallery page. A mixed-media page that can contain media such as images, videos, and other multimedia."""
    type: str = field(default_factory=lambda: "MediaGallery", name="@type")