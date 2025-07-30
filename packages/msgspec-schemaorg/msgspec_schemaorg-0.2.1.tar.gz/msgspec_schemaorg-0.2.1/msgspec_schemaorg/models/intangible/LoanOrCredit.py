from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.FinancialProduct import FinancialProduct
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.RepaymentSpecification import RepaymentSpecification
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class LoanOrCredit(FinancialProduct):
    """A financial product for the loaning of an amount of money, or line of credit, under agreed terms and charges."""
    type: str = field(default_factory=lambda: "LoanOrCredit", name="@type")
    currency: Union[List[str], str, None] = None
    amount: Union[List[Union[int | float, 'MonetaryAmount']], Union[int | float, 'MonetaryAmount'], None] = None
    renegotiableLoan: Union[List[bool], bool, None] = None
    gracePeriod: Union[List['Duration'], 'Duration', None] = None
    loanTerm: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    requiredCollateral: Union[List[Union[str, 'Thing']], Union[str, 'Thing'], None] = None
    recourseLoan: Union[List[bool], bool, None] = None
    loanType: Union[List[Union['URL', str]], Union['URL', str], None] = None
    loanRepaymentForm: Union[List['RepaymentSpecification'], 'RepaymentSpecification', None] = None