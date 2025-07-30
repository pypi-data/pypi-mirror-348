from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
    from msgspec_schemaorg.models.thing.MedicalRiskFactor import MedicalRiskFactor
from typing import Optional, Union, Dict, List, Any


class MedicalRiskEstimator(MedicalEntity):
    """Any rule set or interactive tool for estimating the risk of developing a complication or condition."""
    type: str = field(default_factory=lambda: "MedicalRiskEstimator", name="@type")
    estimatesRiskOf: Union[List['MedicalEntity'], 'MedicalEntity', None] = None
    includedRiskFactor: Union[List['MedicalRiskFactor'], 'MedicalRiskFactor', None] = None