from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.PlaceOfWorship import PlaceOfWorship
from typing import Optional, Union, Dict, List, Any


class Synagogue(PlaceOfWorship):
    """A synagogue."""
    type: str = field(default_factory=lambda: "Synagogue", name="@type")