from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Clip import Clip
from typing import Optional, Union, Dict, List, Any


class VideoGameClip(Clip):
    """A short segment/part of a video game."""
    type: str = field(default_factory=lambda: "VideoGameClip", name="@type")