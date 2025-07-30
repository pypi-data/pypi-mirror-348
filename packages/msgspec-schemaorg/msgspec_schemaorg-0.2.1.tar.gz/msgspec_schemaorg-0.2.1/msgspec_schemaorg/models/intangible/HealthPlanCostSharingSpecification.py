from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
from typing import Optional, Union, Dict, List, Any


class HealthPlanCostSharingSpecification(Intangible):
    """A description of costs to the patient under a given network or formulary."""
    type: str = field(default_factory=lambda: "HealthPlanCostSharingSpecification", name="@type")
    healthPlanPharmacyCategory: Union[List[str], str, None] = None
    healthPlanCoinsuranceOption: Union[List[str], str, None] = None
    healthPlanCopayOption: Union[List[str], str, None] = None
    healthPlanCoinsuranceRate: Union[List[int | float], int | float, None] = None
    healthPlanCopay: Union[List['PriceSpecification'], 'PriceSpecification', None] = None