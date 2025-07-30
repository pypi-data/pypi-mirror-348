from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MemberProgramTier import MemberProgramTier
    from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class PriceSpecification(StructuredValue):
    """A structured value representing a price or price range. Typically, only the subclasses of this type are used for markup. It is recommended to use [[MonetaryAmount]] to describe independent amounts of money such as a salary, credit card limits, etc."""
    type: str = field(default_factory=lambda: "PriceSpecification", name="@type")
    eligibleTransactionVolume: Union[List['PriceSpecification'], 'PriceSpecification', None] = None
    validFrom: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    maxPrice: Union[List[int | float], int | float, None] = None
    priceCurrency: Union[List[str], str, None] = None
    eligibleQuantity: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    membershipPointsEarned: Union[List[Union[int | float, 'QuantitativeValue']], Union[int | float, 'QuantitativeValue'], None] = None
    minPrice: Union[List[int | float], int | float, None] = None
    valueAddedTaxIncluded: Union[List[bool], bool, None] = None
    price: Union[List[Union[int | float, str]], Union[int | float, str], None] = None
    validForMemberTier: Union[List['MemberProgramTier'], 'MemberProgramTier', None] = None
    validThrough: Union[List[Union[datetime, date]], Union[datetime, date], None] = None