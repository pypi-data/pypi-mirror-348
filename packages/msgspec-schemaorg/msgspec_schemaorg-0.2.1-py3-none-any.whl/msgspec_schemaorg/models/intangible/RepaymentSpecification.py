from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
from typing import Optional, Union, Dict, List, Any


class RepaymentSpecification(StructuredValue):
    """A structured value representing repayment."""
    type: str = field(default_factory=lambda: "RepaymentSpecification", name="@type")
    loanPaymentFrequency: Union[List[int | float], int | float, None] = None
    downPayment: Union[List[Union[int | float, 'MonetaryAmount']], Union[int | float, 'MonetaryAmount'], None] = None
    numberOfLoanPayments: Union[List[int | float], int | float, None] = None
    loanPaymentAmount: Union[List['MonetaryAmount'], 'MonetaryAmount', None] = None
    earlyPrepaymentPenalty: Union[List['MonetaryAmount'], 'MonetaryAmount', None] = None