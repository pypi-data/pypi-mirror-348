from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.MediaObject import MediaObject
from typing import Optional, Union, Dict, List, Any


class MusicVideoObject(MediaObject):
    """A music video file."""
    type: str = field(default_factory=lambda: "MusicVideoObject", name="@type")