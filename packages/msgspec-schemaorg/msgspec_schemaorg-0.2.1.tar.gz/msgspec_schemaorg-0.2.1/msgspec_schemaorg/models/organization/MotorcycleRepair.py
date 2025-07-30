from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.AutomotiveBusiness import AutomotiveBusiness
from typing import Optional, Union, Dict, List, Any


class MotorcycleRepair(AutomotiveBusiness):
    """A motorcycle repair shop."""
    type: str = field(default_factory=lambda: "MotorcycleRepair", name="@type")