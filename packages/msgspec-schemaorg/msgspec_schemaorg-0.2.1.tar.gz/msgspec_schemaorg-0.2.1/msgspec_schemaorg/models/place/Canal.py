from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.BodyOfWater import BodyOfWater
from typing import Optional, Union, Dict, List, Any


class Canal(BodyOfWater):
    """A canal, like the Panama Canal."""
    type: str = field(default_factory=lambda: "Canal", name="@type")