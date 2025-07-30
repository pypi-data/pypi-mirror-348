from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Landform import Landform
from typing import Optional, Union, Dict, List, Any


class Mountain(Landform):
    """A mountain, like Mount Whitney or Mount Everest."""
    type: str = field(default_factory=lambda: "Mountain", name="@type")