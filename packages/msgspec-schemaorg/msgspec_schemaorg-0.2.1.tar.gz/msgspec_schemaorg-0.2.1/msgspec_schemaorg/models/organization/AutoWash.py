from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.AutomotiveBusiness import AutomotiveBusiness
from typing import Optional, Union, Dict, List, Any


class AutoWash(AutomotiveBusiness):
    """A car wash business."""
    type: str = field(default_factory=lambda: "AutoWash", name="@type")