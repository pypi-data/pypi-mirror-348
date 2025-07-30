from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Landform import Landform
from typing import Optional, Union, Dict, List, Any


class Continent(Landform):
    """One of the continents (for example, Europe or Africa)."""
    type: str = field(default_factory=lambda: "Continent", name="@type")