from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.BodyOfWater import BodyOfWater
from typing import Optional, Union, Dict, List, Any


class LakeBodyOfWater(BodyOfWater):
    """A lake (for example, Lake Pontrachain)."""
    type: str = field(default_factory=lambda: "LakeBodyOfWater", name="@type")