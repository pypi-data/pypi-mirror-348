from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class DatedMoneySpecification(StructuredValue):
    """A DatedMoneySpecification represents monetary values with optional start and end dates. For example, this could represent an employee's salary over a specific period of time. __Note:__ This type has been superseded by [[MonetaryAmount]], use of that type is recommended."""
    type: str = field(default_factory=lambda: "DatedMoneySpecification", name="@type")
    currency: Union[List[str], str, None] = None
    amount: Union[List[Union[int | float, 'MonetaryAmount']], Union[int | float, 'MonetaryAmount'], None] = None
    endDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    startDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None