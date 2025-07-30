from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.product.Vehicle import Vehicle
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class Car(Vehicle):
    """A car is a wheeled, self-powered motor vehicle used for transportation."""
    type: str = field(default_factory=lambda: "Car", name="@type")
    roofLoad: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    acrissCode: Union[List[str], str, None] = None