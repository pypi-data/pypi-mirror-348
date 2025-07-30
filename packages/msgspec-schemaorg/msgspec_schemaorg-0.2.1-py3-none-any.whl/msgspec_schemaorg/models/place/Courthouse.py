from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.GovernmentBuilding import GovernmentBuilding
from typing import Optional, Union, Dict, List, Any


class Courthouse(GovernmentBuilding):
    """A courthouse."""
    type: str = field(default_factory=lambda: "Courthouse", name="@type")