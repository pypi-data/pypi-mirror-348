from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.FoodEstablishment import FoodEstablishment
from typing import Optional, Union, Dict, List, Any


class Winery(FoodEstablishment):
    """A winery."""
    type: str = field(default_factory=lambda: "Winery", name="@type")