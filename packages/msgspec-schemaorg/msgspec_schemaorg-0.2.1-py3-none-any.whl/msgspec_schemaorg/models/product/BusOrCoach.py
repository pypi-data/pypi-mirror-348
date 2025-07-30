from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.product.Vehicle import Vehicle
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class BusOrCoach(Vehicle):
    """A bus (also omnibus or autobus) is a road vehicle designed to carry passengers. Coaches are luxury buses, usually in service for long distance travel."""
    type: str = field(default_factory=lambda: "BusOrCoach", name="@type")
    roofLoad: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    acrissCode: Union[List[str], str, None] = None