from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.MediaObject import MediaObject
from typing import Optional, Union, Dict, List, Any


class AmpStory(MediaObject):
    """A creative work with a visual storytelling format intended to be viewed online, particularly on mobile devices."""
    type: str = field(default_factory=lambda: "AmpStory", name="@type")