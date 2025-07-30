from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.DeliveryMethod import DeliveryMethod
    from msgspec_schemaorg.models.intangible.PaymentMethod import PaymentMethod
from typing import Optional, Union, Dict, List, Any


class PaymentChargeSpecification(PriceSpecification):
    """The costs of settling the payment using a particular payment method."""
    type: str = field(default_factory=lambda: "PaymentChargeSpecification", name="@type")
    appliesToPaymentMethod: Union[List['PaymentMethod'], 'PaymentMethod', None] = None
    appliesToDeliveryMethod: Union[List['DeliveryMethod'], 'DeliveryMethod', None] = None