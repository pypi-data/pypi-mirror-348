from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.FinancialProduct import FinancialProduct
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
from typing import Optional, Union, Dict, List, Any


class InvestmentOrDeposit(FinancialProduct):
    """A type of financial product that typically requires the client to transfer funds to a financial service in return for potential beneficial financial return."""
    type: str = field(default_factory=lambda: "InvestmentOrDeposit", name="@type")
    amount: Union[List[Union[int | float, 'MonetaryAmount']], Union[int | float, 'MonetaryAmount'], None] = None