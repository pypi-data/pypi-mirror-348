from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.GovernmentBuilding import GovernmentBuilding
from typing import Optional, Union, Dict, List, Any


class Embassy(GovernmentBuilding):
    """An embassy."""
    type: str = field(default_factory=lambda: "Embassy", name="@type")