from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.HomeAndConstructionBusiness import HomeAndConstructionBusiness
from typing import Optional, Union, Dict, List, Any


class HVACBusiness(HomeAndConstructionBusiness):
    """A business that provides Heating, Ventilation and Air Conditioning services."""
    type: str = field(default_factory=lambda: "HVACBusiness", name="@type")