from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.PriceTypeEnumeration import PriceTypeEnumeration
    from msgspec_schemaorg.models.intangible.UnitPriceSpecification import UnitPriceSpecification
from typing import Optional, Union, Dict, List, Any


class CompoundPriceSpecification(PriceSpecification):
    """A compound price specification is one that bundles multiple prices that all apply in combination for different dimensions of consumption. Use the name property of the attached unit price specification for indicating the dimension of a price component (e.g. "electricity" or "final cleaning")."""
    type: str = field(default_factory=lambda: "CompoundPriceSpecification", name="@type")
    priceType: Union[List[Union[str, 'PriceTypeEnumeration']], Union[str, 'PriceTypeEnumeration'], None] = None
    priceComponent: Union[List['UnitPriceSpecification'], 'UnitPriceSpecification', None] = None