from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Reservation import Reservation
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from datetime import datetime, time
from typing import Optional, Union, Dict, List, Any


class FoodEstablishmentReservation(Reservation):
    """A reservation to dine at a food-related business.\\n\\nNote: This type is for information about actual reservations, e.g. in confirmation emails or HTML pages with individual confirmations of reservations."""
    type: str = field(default_factory=lambda: "FoodEstablishmentReservation", name="@type")
    startTime: Union[List[Union[datetime, time]], Union[datetime, time], None] = None
    partySize: Union[List[Union[int, 'QuantitativeValue']], Union[int, 'QuantitativeValue'], None] = None
    endTime: Union[List[Union[datetime, time]], Union[datetime, time], None] = None