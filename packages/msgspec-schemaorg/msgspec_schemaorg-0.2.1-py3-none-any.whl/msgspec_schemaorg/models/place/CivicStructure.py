from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Place import Place
from typing import Optional, Union, Dict, List, Any


class CivicStructure(Place):
    """A public structure, such as a town hall or concert hall."""
    type: str = field(default_factory=lambda: "CivicStructure", name="@type")
    openingHours: Union[List[str], str, None] = None