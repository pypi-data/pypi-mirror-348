from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Place import Place
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.FloorPlan import FloorPlan
from typing import Optional, Union, Dict, List, Any


class Residence(Place):
    """The place where a person lives."""
    type: str = field(default_factory=lambda: "Residence", name="@type")
    accommodationFloorPlan: Union[List['FloorPlan'], 'FloorPlan', None] = None