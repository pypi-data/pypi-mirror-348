from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.CreditCard import CreditCard
    from msgspec_schemaorg.models.intangible.MemberProgram import MemberProgram
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.enums.intangible.TierBenefitEnumeration import TierBenefitEnumeration
    from msgspec_schemaorg.models.intangible.UnitPriceSpecification import UnitPriceSpecification
from typing import Optional, Union, Dict, List, Any


class MemberProgramTier(Intangible):
    """A MemberProgramTier specifies a tier under a loyalty (member) program, for example "gold"."""
    type: str = field(default_factory=lambda: "MemberProgramTier", name="@type")
    hasTierBenefit: Union[List['TierBenefitEnumeration'], 'TierBenefitEnumeration', None] = None
    membershipPointsEarned: Union[List[Union[int | float, 'QuantitativeValue']], Union[int | float, 'QuantitativeValue'], None] = None
    hasTierRequirement: Union[List[Union[str, 'CreditCard', 'MonetaryAmount', 'UnitPriceSpecification']], Union[str, 'CreditCard', 'MonetaryAmount', 'UnitPriceSpecification'], None] = None
    isTierOf: Union[List['MemberProgram'], 'MemberProgram', None] = None