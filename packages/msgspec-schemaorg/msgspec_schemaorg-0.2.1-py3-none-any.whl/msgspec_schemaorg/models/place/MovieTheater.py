from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.CivicStructure import CivicStructure
from typing import Optional, Union, Dict, List, Any


class MovieTheater(CivicStructure):
    """A movie theater."""
    type: str = field(default_factory=lambda: "MovieTheater", name="@type")
    screenCount: Union[List[int | float], int | float, None] = None