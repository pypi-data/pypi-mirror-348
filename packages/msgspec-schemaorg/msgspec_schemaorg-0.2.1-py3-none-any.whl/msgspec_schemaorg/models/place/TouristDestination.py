from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Place import Place
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.place.TouristAttraction import TouristAttraction
from typing import Optional, Union, Dict, List, Any


class TouristDestination(Place):
    """A tourist destination. In principle any [[Place]] can be a [[TouristDestination]] from a [[City]], Region or [[Country]] to an [[AmusementPark]] or [[Hotel]]. This Type can be used on its own to describe a general [[TouristDestination]], or be used as an [[additionalType]] to add tourist relevant properties to any other [[Place]].  A [[TouristDestination]] is defined as a [[Place]] that contains, or is colocated with, one or more [[TouristAttraction]]s, often linked by a similar theme or interest to a particular [[touristType]]. The [UNWTO](http://www2.unwto.org/) defines Destination (main destination of a tourism trip) as the place visited that is central to the decision to take the trip.
  (See examples below.)"""
    type: str = field(default_factory=lambda: "TouristDestination", name="@type")
    touristType: Union[List[Union[str, 'Audience']], Union[str, 'Audience'], None] = None
    includesAttraction: Union[List['TouristAttraction'], 'TouristAttraction', None] = None