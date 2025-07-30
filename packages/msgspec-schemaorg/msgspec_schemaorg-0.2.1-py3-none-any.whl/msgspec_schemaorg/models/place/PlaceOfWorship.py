from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.CivicStructure import CivicStructure
from typing import Optional, Union, Dict, List, Any


class PlaceOfWorship(CivicStructure):
    """Place of worship, such as a church, synagogue, or mosque."""
    type: str = field(default_factory=lambda: "PlaceOfWorship", name="@type")