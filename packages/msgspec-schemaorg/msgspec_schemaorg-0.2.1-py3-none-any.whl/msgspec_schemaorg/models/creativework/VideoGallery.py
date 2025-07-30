from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.MediaGallery import MediaGallery
from typing import Optional, Union, Dict, List, Any


class VideoGallery(MediaGallery):
    """Web page type: Video gallery page."""
    type: str = field(default_factory=lambda: "VideoGallery", name="@type")