from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.BodyOfWater import BodyOfWater
from typing import Optional, Union, Dict, List, Any


class OceanBodyOfWater(BodyOfWater):
    """An ocean (for example, the Pacific)."""
    type: str = field(default_factory=lambda: "OceanBodyOfWater", name="@type")