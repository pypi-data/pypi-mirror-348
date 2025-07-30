from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.CivicStructure import CivicStructure
from typing import Optional, Union, Dict, List, Any


class GovernmentBuilding(CivicStructure):
    """A government building."""
    type: str = field(default_factory=lambda: "GovernmentBuilding", name="@type")