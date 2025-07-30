from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import Optional, Union, Dict, List, Any


class HealthPlanFormulary(Intangible):
    """For a given health insurance plan, the specification for costs and coverage of prescription drugs."""
    type: str = field(default_factory=lambda: "HealthPlanFormulary", name="@type")
    offersPrescriptionByMail: Union[List[bool], bool, None] = None
    healthPlanCostSharing: Union[List[bool], bool, None] = None
    healthPlanDrugTier: Union[List[str], str, None] = None