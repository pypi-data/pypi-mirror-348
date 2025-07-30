from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.ContactPoint import ContactPoint
    from msgspec_schemaorg.models.intangible.HealthPlanFormulary import HealthPlanFormulary
    from msgspec_schemaorg.models.intangible.HealthPlanNetwork import HealthPlanNetwork
from typing import Optional, Union, Dict, List, Any


class HealthInsurancePlan(Intangible):
    """A US-style health insurance plan, including PPOs, EPOs, and HMOs."""
    type: str = field(default_factory=lambda: "HealthInsurancePlan", name="@type")
    healthPlanDrugOption: Union[List[str], str, None] = None
    healthPlanId: Union[List[str], str, None] = None
    healthPlanMarketingUrl: Union[List['URL'], 'URL', None] = None
    healthPlanDrugTier: Union[List[str], str, None] = None
    usesHealthPlanIdStandard: Union[List[Union['URL', str]], Union['URL', str], None] = None
    includesHealthPlanFormulary: Union[List['HealthPlanFormulary'], 'HealthPlanFormulary', None] = None
    contactPoint: Union[List['ContactPoint'], 'ContactPoint', None] = None
    benefitsSummaryUrl: Union[List['URL'], 'URL', None] = None
    includesHealthPlanNetwork: Union[List['HealthPlanNetwork'], 'HealthPlanNetwork', None] = None