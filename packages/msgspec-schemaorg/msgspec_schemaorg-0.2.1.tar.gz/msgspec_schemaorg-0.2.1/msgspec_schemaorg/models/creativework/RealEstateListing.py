from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.WebPage import WebPage
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class RealEstateListing(WebPage):
    """A [[RealEstateListing]] is a listing that describes one or more real-estate [[Offer]]s (whose [[businessFunction]] is typically to lease out, or to sell).
  The [[RealEstateListing]] type itself represents the overall listing, as manifested in some [[WebPage]].
  """
    type: str = field(default_factory=lambda: "RealEstateListing", name="@type")
    datePosted: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    leaseLength: Union[List[Union['Duration', 'QuantitativeValue']], Union['Duration', 'QuantitativeValue'], None] = None