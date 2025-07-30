from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.PaymentMethod import PaymentMethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
from typing import Optional, Union, Dict, List, Any


class PaymentCard(PaymentMethod):
    """A payment method using a credit, debit, store or other card to associate the payment with an account."""
    type: str = field(default_factory=lambda: "PaymentCard", name="@type")
    contactlessPayment: Union[List[bool], bool, None] = None
    floorLimit: Union[List['MonetaryAmount'], 'MonetaryAmount', None] = None
    cashBack: Union[List[Union[int | float, bool]], Union[int | float, bool], None] = None
    monthlyMinimumRepaymentAmount: Union[List[Union[int | float, 'MonetaryAmount']], Union[int | float, 'MonetaryAmount'], None] = None