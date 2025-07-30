from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.MediaGallery import MediaGallery
from typing import Optional, Union, Dict, List, Any


class ImageGallery(MediaGallery):
    """Web page type: Image gallery page."""
    type: str = field(default_factory=lambda: "ImageGallery", name="@type")