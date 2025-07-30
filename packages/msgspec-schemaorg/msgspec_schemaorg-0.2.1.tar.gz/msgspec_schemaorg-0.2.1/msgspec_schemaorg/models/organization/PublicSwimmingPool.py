from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.SportsActivityLocation import SportsActivityLocation
from typing import Optional, Union, Dict, List, Any


class PublicSwimmingPool(SportsActivityLocation):
    """A public swimming pool."""
    type: str = field(default_factory=lambda: "PublicSwimmingPool", name="@type")