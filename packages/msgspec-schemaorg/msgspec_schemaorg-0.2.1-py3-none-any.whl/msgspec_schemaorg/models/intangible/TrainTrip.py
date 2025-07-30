from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Trip import Trip
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.place.TrainStation import TrainStation
from typing import Optional, Union, Dict, List, Any


class TrainTrip(Trip):
    """A trip on a commercial train line."""
    type: str = field(default_factory=lambda: "TrainTrip", name="@type")
    arrivalStation: Union[List['TrainStation'], 'TrainStation', None] = None
    departureStation: Union[List['TrainStation'], 'TrainStation', None] = None
    trainNumber: Union[List[str], str, None] = None
    departurePlatform: Union[List[str], str, None] = None
    trainName: Union[List[str], str, None] = None
    arrivalPlatform: Union[List[str], str, None] = None