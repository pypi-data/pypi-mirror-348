from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.GovernmentBuilding import GovernmentBuilding
from typing import Optional, Union, Dict, List, Any


class DefenceEstablishment(GovernmentBuilding):
    """A defence establishment, such as an army or navy base."""
    type: str = field(default_factory=lambda: "DefenceEstablishment", name="@type")