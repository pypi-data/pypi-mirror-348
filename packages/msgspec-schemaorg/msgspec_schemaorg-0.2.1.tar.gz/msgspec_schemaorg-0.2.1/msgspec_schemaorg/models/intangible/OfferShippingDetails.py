from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DefinedRegion import DefinedRegion
    from msgspec_schemaorg.models.intangible.Distance import Distance
    from msgspec_schemaorg.models.intangible.Mass import Mass
    from msgspec_schemaorg.models.intangible.MemberProgramTier import MemberProgramTier
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.ShippingDeliveryTime import ShippingDeliveryTime
    from msgspec_schemaorg.models.intangible.ShippingRateSettings import ShippingRateSettings
    from msgspec_schemaorg.models.intangible.ShippingService import ShippingService
from typing import Optional, Union, Dict, List, Any


class OfferShippingDetails(StructuredValue):
    """OfferShippingDetails represents information about shipping destinations.

Multiple of these entities can be used to represent different shipping rates for different destinations:

One entity for Alaska/Hawaii. A different one for continental US. A different one for all France.

Multiple of these entities can be used to represent different shipping costs and delivery times.

Two entities that are identical but differ in rate and time:

E.g. Cheaper and slower: $5 in 5-7 days
or Fast and expensive: $15 in 1-2 days."""
    type: str = field(default_factory=lambda: "OfferShippingDetails", name="@type")
    deliveryTime: Union[List['ShippingDeliveryTime'], 'ShippingDeliveryTime', None] = None
    shippingRate: Union[List[Union['ShippingRateSettings', 'MonetaryAmount']], Union['ShippingRateSettings', 'MonetaryAmount'], None] = None
    shippingDestination: Union[List['DefinedRegion'], 'DefinedRegion', None] = None
    hasShippingService: Union[List['ShippingService'], 'ShippingService', None] = None
    height: Union[List[Union['Distance', 'QuantitativeValue']], Union['Distance', 'QuantitativeValue'], None] = None
    shippingOrigin: Union[List['DefinedRegion'], 'DefinedRegion', None] = None
    width: Union[List[Union['Distance', 'QuantitativeValue']], Union['Distance', 'QuantitativeValue'], None] = None
    depth: Union[List[Union['QuantitativeValue', 'Distance']], Union['QuantitativeValue', 'Distance'], None] = None
    weight: Union[List[Union['Mass', 'QuantitativeValue']], Union['Mass', 'QuantitativeValue'], None] = None
    validForMemberTier: Union[List['MemberProgramTier'], 'MemberProgramTier', None] = None
    doesNotShip: Union[List[bool], bool, None] = None