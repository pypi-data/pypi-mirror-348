from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.WarrantyScope import WarrantyScope
from typing import Optional, Union, Dict, List, Any


class WarrantyPromise(StructuredValue):
    """A structured value representing the duration and scope of services that will be provided to a customer free of charge in case of a defect or malfunction of a product."""
    type: str = field(default_factory=lambda: "WarrantyPromise", name="@type")
    durationOfWarranty: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    warrantyScope: Union[List['WarrantyScope'], 'WarrantyScope', None] = None