from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.CivicStructure import CivicStructure
from typing import Optional, Union, Dict, List, Any


class BusStop(CivicStructure):
    """A bus stop."""
    type: str = field(default_factory=lambda: "BusStop", name="@type")