from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.BodyOfWater import BodyOfWater
from typing import Optional, Union, Dict, List, Any


class SeaBodyOfWater(BodyOfWater):
    """A sea (for example, the Caspian sea)."""
    type: str = field(default_factory=lambda: "SeaBodyOfWater", name="@type")