from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.VisualArtwork import VisualArtwork
from typing import Optional, Union, Dict, List, Any


class CoverArt(VisualArtwork):
    """The artwork on the outer surface of a CreativeWork."""
    type: str = field(default_factory=lambda: "CoverArt", name="@type")