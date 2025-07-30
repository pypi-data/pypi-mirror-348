from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.PerformingGroup import PerformingGroup
from typing import Optional, Union, Dict, List, Any


class DanceGroup(PerformingGroup):
    """A dance group&#x2014;for example, the Alvin Ailey Dance Theater or Riverdance."""
    type: str = field(default_factory=lambda: "DanceGroup", name="@type")