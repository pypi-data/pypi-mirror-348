from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.AutomotiveBusiness import AutomotiveBusiness
from typing import Optional, Union, Dict, List, Any


class AutoRental(AutomotiveBusiness):
    """A car rental business."""
    type: str = field(default_factory=lambda: "AutoRental", name="@type")