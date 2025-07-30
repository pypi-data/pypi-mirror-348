from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.product.Product import Product
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.product.ProductGroup import ProductGroup
    from msgspec_schemaorg.models.product.ProductModel import ProductModel
from typing import Optional, Union, Dict, List, Any


class ProductModel(Product):
    """A datasheet or vendor specification of a product (in the sense of a prototypical description)."""
    type: str = field(default_factory=lambda: "ProductModel", name="@type")
    successorOf: Union[List['ProductModel'], 'ProductModel', None] = None
    isVariantOf: Union[List[Union['ProductModel', 'ProductGroup']], Union['ProductModel', 'ProductGroup'], None] = None
    predecessorOf: Union[List['ProductModel'], 'ProductModel', None] = None