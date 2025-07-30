from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.HomeAndConstructionBusiness import HomeAndConstructionBusiness
from typing import Optional, Union, Dict, List, Any


class HousePainter(HomeAndConstructionBusiness):
    """A house painting service."""
    type: str = field(default_factory=lambda: "HousePainter", name="@type")