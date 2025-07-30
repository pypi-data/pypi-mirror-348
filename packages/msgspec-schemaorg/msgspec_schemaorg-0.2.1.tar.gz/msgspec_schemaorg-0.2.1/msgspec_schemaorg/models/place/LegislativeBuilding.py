from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.GovernmentBuilding import GovernmentBuilding
from typing import Optional, Union, Dict, List, Any


class LegislativeBuilding(GovernmentBuilding):
    """A legislative building&#x2014;for example, the state capitol."""
    type: str = field(default_factory=lambda: "LegislativeBuilding", name="@type")