from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.HealthAndBeautyBusiness import HealthAndBeautyBusiness
from typing import Optional, Union, Dict, List, Any


class DaySpa(HealthAndBeautyBusiness):
    """A day spa."""
    type: str = field(default_factory=lambda: "DaySpa", name="@type")