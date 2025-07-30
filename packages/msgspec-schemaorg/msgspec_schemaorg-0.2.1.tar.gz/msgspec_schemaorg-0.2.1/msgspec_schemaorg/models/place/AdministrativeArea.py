from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Place import Place
from typing import Optional, Union, Dict, List, Any


class AdministrativeArea(Place):
    """A geographical region, typically under the jurisdiction of a particular government."""
    type: str = field(default_factory=lambda: "AdministrativeArea", name="@type")