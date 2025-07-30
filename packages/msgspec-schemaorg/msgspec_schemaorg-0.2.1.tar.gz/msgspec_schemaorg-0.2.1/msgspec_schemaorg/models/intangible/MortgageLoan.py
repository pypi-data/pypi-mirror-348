from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.LoanOrCredit import LoanOrCredit
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
from typing import Optional, Union, Dict, List, Any


class MortgageLoan(LoanOrCredit):
    """A loan in which property or real estate is used as collateral. (A loan securitized against some real estate.)"""
    type: str = field(default_factory=lambda: "MortgageLoan", name="@type")
    loanMortgageMandateAmount: Union[List['MonetaryAmount'], 'MonetaryAmount', None] = None
    domiciledMortgage: Union[List[bool], bool, None] = None