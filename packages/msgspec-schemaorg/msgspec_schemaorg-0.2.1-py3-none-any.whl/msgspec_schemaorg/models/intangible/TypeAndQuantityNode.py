from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.BusinessFunction import BusinessFunction
    from msgspec_schemaorg.models.intangible.Service import Service
    from msgspec_schemaorg.models.product.Product import Product
from typing import Optional, Union, Dict, List, Any


class TypeAndQuantityNode(StructuredValue):
    """A structured value indicating the quantity, unit of measurement, and business function of goods included in a bundle offer."""
    type: str = field(default_factory=lambda: "TypeAndQuantityNode", name="@type")
    amountOfThisGood: Union[List[int | float], int | float, None] = None
    businessFunction: Union[List['BusinessFunction'], 'BusinessFunction', None] = None
    unitText: Union[List[str], str, None] = None
    typeOfGood: Union[List[Union['Product', 'Service']], Union['Product', 'Service'], None] = None
    unitCode: Union[List[Union['URL', str]], Union['URL', str], None] = None