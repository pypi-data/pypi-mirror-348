from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Audience import Audience
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class BusinessAudience(Audience):
    """A set of characteristics belonging to businesses, e.g. who compose an item's target audience."""
    type: str = field(default_factory=lambda: "BusinessAudience", name="@type")
    numberOfEmployees: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    yearsInOperation: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    yearlyRevenue: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None