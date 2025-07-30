from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.product.Product import Product
from typing import Optional, Union, Dict, List, Any


class IndividualProduct(Product):
    """A single, identifiable product instance (e.g. a laptop with a particular serial number)."""
    type: str = field(default_factory=lambda: "IndividualProduct", name="@type")
    serialNumber: Union[List[str], str, None] = None