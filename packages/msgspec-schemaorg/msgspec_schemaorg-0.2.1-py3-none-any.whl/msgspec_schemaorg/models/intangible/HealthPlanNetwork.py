from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import Optional, Union, Dict, List, Any


class HealthPlanNetwork(Intangible):
    """A US-style health insurance plan network."""
    type: str = field(default_factory=lambda: "HealthPlanNetwork", name="@type")
    healthPlanNetworkId: Union[List[str], str, None] = None
    healthPlanCostSharing: Union[List[bool], bool, None] = None
    healthPlanNetworkTier: Union[List[str], str, None] = None