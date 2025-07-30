from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.intangible.UnitPriceSpecification import UnitPriceSpecification
from typing import Optional, Union, Dict, List, Any


class ExchangeRateSpecification(StructuredValue):
    """A structured value representing exchange rate."""
    type: str = field(default_factory=lambda: "ExchangeRateSpecification", name="@type")
    currency: Union[List[str], str, None] = None
    currentExchangeRate: Union[List['UnitPriceSpecification'], 'UnitPriceSpecification', None] = None
    exchangeRateSpread: Union[List[Union[int | float, 'MonetaryAmount']], Union[int | float, 'MonetaryAmount'], None] = None