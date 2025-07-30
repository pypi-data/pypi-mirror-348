from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.enums.intangible.PriceComponentTypeEnumeration import PriceComponentTypeEnumeration
    from msgspec_schemaorg.enums.intangible.PriceTypeEnumeration import PriceTypeEnumeration
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class UnitPriceSpecification(PriceSpecification):
    """The price asked for a given offer by the respective organization or person."""
    type: str = field(default_factory=lambda: "UnitPriceSpecification", name="@type")
    billingIncrement: Union[List[int | float], int | float, None] = None
    priceType: Union[List[Union[str, 'PriceTypeEnumeration']], Union[str, 'PriceTypeEnumeration'], None] = None
    unitText: Union[List[str], str, None] = None
    referenceQuantity: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    billingDuration: Union[List[Union[int | float, 'Duration', 'QuantitativeValue']], Union[int | float, 'Duration', 'QuantitativeValue'], None] = None
    unitCode: Union[List[Union['URL', str]], Union['URL', str], None] = None
    billingStart: Union[List[int | float], int | float, None] = None
    priceComponentType: Union[List['PriceComponentTypeEnumeration'], 'PriceComponentTypeEnumeration', None] = None