from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Place import Place
from typing import Optional, Union, Dict, List, Any


class LandmarksOrHistoricalBuildings(Place):
    """An historical landmark or building."""
    type: str = field(default_factory=lambda: "LandmarksOrHistoricalBuildings", name="@type")