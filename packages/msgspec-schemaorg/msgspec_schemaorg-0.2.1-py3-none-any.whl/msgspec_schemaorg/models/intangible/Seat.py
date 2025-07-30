from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.QualitativeValue import QualitativeValue
from typing import Optional, Union, Dict, List, Any


class Seat(Intangible):
    """Used to describe a seat, such as a reserved seat in an event reservation."""
    type: str = field(default_factory=lambda: "Seat", name="@type")
    seatSection: Union[List[str], str, None] = None
    seatRow: Union[List[str], str, None] = None
    seatingType: Union[List[Union[str, 'QualitativeValue']], Union[str, 'QualitativeValue'], None] = None
    seatNumber: Union[List[str], str, None] = None