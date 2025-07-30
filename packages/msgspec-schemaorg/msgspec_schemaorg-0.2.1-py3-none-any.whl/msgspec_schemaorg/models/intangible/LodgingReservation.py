from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Reservation import Reservation
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.QualitativeValue import QualitativeValue
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from datetime import datetime, time
from typing import Optional, Union, Dict, List, Any


class LodgingReservation(Reservation):
    """A reservation for lodging at a hotel, motel, inn, etc.\\n\\nNote: This type is for information about actual reservations, e.g. in confirmation emails or HTML pages with individual confirmations of reservations."""
    type: str = field(default_factory=lambda: "LodgingReservation", name="@type")
    lodgingUnitType: Union[List[Union[str, 'QualitativeValue']], Union[str, 'QualitativeValue'], None] = None
    lodgingUnitDescription: Union[List[str], str, None] = None
    numChildren: Union[List[Union[int, 'QuantitativeValue']], Union[int, 'QuantitativeValue'], None] = None
    numAdults: Union[List[Union[int, 'QuantitativeValue']], Union[int, 'QuantitativeValue'], None] = None
    checkoutTime: Union[List[Union[datetime, time]], Union[datetime, time], None] = None
    checkinTime: Union[List[Union[datetime, time]], Union[datetime, time], None] = None