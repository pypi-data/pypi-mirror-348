from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.product.Product import Product
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class SomeProducts(Product):
    """A placeholder for multiple similar products of the same kind."""
    type: str = field(default_factory=lambda: "SomeProducts", name="@type")
    inventoryLevel: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None