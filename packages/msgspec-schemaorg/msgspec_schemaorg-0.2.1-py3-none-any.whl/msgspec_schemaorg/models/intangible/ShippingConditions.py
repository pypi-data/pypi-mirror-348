from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DefinedRegion import DefinedRegion
    from msgspec_schemaorg.models.intangible.Distance import Distance
    from msgspec_schemaorg.models.intangible.Mass import Mass
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.intangible.OpeningHoursSpecification import OpeningHoursSpecification
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.ServicePeriod import ServicePeriod
    from msgspec_schemaorg.models.intangible.ShippingRateSettings import ShippingRateSettings
from typing import Optional, Union, Dict, List, Any


class ShippingConditions(StructuredValue):
    """ShippingConditions represent a set of constraints and information about the conditions of shipping a product. Such conditions may apply to only a subset of the products being shipped, depending on aspects of the product like weight, size, price, destination, and others. All the specified conditions must be met for this ShippingConditions to apply."""
    type: str = field(default_factory=lambda: "ShippingConditions", name="@type")
    shippingRate: Union[List[Union['ShippingRateSettings', 'MonetaryAmount']], Union['ShippingRateSettings', 'MonetaryAmount'], None] = None
    shippingDestination: Union[List['DefinedRegion'], 'DefinedRegion', None] = None
    transitTime: Union[List[Union['QuantitativeValue', 'ServicePeriod']], Union['QuantitativeValue', 'ServicePeriod'], None] = None
    height: Union[List[Union['Distance', 'QuantitativeValue']], Union['Distance', 'QuantitativeValue'], None] = None
    seasonalOverride: Union[List['OpeningHoursSpecification'], 'OpeningHoursSpecification', None] = None
    shippingOrigin: Union[List['DefinedRegion'], 'DefinedRegion', None] = None
    numItems: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    width: Union[List[Union['Distance', 'QuantitativeValue']], Union['Distance', 'QuantitativeValue'], None] = None
    orderValue: Union[List['MonetaryAmount'], 'MonetaryAmount', None] = None
    depth: Union[List[Union['QuantitativeValue', 'Distance']], Union['QuantitativeValue', 'Distance'], None] = None
    weight: Union[List[Union['Mass', 'QuantitativeValue']], Union['Mass', 'QuantitativeValue'], None] = None
    doesNotShip: Union[List[bool], bool, None] = None