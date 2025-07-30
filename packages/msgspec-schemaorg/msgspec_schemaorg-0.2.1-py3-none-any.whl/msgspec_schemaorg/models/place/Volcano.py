from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Landform import Landform
from typing import Optional, Union, Dict, List, Any


class Volcano(Landform):
    """A volcano, like Fujisan."""
    type: str = field(default_factory=lambda: "Volcano", name="@type")