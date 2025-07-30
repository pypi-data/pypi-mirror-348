from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DefinedRegion import DefinedRegion
    from msgspec_schemaorg.models.intangible.DeliveryChargeSpecification import DeliveryChargeSpecification
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.intangible.ShippingRateSettings import ShippingRateSettings
from typing import Optional, Union, Dict, List, Any


class ShippingRateSettings(StructuredValue):
    """A ShippingRateSettings represents re-usable pieces of shipping information. It is designed for publication on an URL that may be referenced via the [[shippingSettingsLink]] property of an [[OfferShippingDetails]]. Several occurrences can be published, distinguished and matched (i.e. identified/referenced) by their different values for [[shippingLabel]]."""
    type: str = field(default_factory=lambda: "ShippingRateSettings", name="@type")
    shippingRate: Union[List[Union['ShippingRateSettings', 'MonetaryAmount']], Union['ShippingRateSettings', 'MonetaryAmount'], None] = None
    shippingDestination: Union[List['DefinedRegion'], 'DefinedRegion', None] = None
    weightPercentage: Union[List[int | float], int | float, None] = None
    isUnlabelledFallback: Union[List[bool], bool, None] = None
    freeShippingThreshold: Union[List[Union['DeliveryChargeSpecification', 'MonetaryAmount']], Union['DeliveryChargeSpecification', 'MonetaryAmount'], None] = None
    orderPercentage: Union[List[int | float], int | float, None] = None
    doesNotShip: Union[List[bool], bool, None] = None