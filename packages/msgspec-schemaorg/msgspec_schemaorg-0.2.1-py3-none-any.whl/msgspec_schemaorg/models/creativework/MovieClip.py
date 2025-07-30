from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Clip import Clip
from typing import Optional, Union, Dict, List, Any


class MovieClip(Clip):
    """A short segment/part of a movie."""
    type: str = field(default_factory=lambda: "MovieClip", name="@type")