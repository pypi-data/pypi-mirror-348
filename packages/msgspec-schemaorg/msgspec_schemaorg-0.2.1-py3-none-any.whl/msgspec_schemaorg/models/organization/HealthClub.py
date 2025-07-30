from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.HealthAndBeautyBusiness import HealthAndBeautyBusiness
from typing import Optional, Union, Dict, List, Any


class HealthClub(HealthAndBeautyBusiness):
    """A health club."""
    type: str = field(default_factory=lambda: "HealthClub", name="@type")