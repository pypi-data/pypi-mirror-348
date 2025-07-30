from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.GovernmentBuilding import GovernmentBuilding
from typing import Optional, Union, Dict, List, Any


class CityHall(GovernmentBuilding):
    """A city hall."""
    type: str = field(default_factory=lambda: "CityHall", name="@type")