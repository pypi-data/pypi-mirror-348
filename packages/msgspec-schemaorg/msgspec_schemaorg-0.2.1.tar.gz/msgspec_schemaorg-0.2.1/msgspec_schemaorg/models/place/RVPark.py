from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.CivicStructure import CivicStructure
from typing import Optional, Union, Dict, List, Any


class RVPark(CivicStructure):
    """A place offering space for "Recreational Vehicles", Caravans, mobile homes and the like."""
    type: str = field(default_factory=lambda: "RVPark", name="@type")