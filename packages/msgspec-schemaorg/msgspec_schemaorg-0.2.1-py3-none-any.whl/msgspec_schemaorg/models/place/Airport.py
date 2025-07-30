from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.CivicStructure import CivicStructure
from typing import Optional, Union, Dict, List, Any


class Airport(CivicStructure):
    """An airport."""
    type: str = field(default_factory=lambda: "Airport", name="@type")
    iataCode: Union[List[str], str, None] = None
    icaoCode: Union[List[str], str, None] = None