from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.product.Product import Product
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.TypeAndQuantityNode import TypeAndQuantityNode
from typing import Optional, Union, Dict, List, Any


class ProductCollection(Product):
    """A set of products (either [[ProductGroup]]s or specific variants) that are listed together e.g. in an [[Offer]]."""
    type: str = field(default_factory=lambda: "ProductCollection", name="@type")
    includesObject: Union[List['TypeAndQuantityNode'], 'TypeAndQuantityNode', None] = None