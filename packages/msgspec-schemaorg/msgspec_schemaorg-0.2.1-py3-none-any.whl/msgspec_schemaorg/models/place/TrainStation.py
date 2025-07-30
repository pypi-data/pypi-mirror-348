from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.CivicStructure import CivicStructure
from typing import Optional, Union, Dict, List, Any


class TrainStation(CivicStructure):
    """A train station."""
    type: str = field(default_factory=lambda: "TrainStation", name="@type")