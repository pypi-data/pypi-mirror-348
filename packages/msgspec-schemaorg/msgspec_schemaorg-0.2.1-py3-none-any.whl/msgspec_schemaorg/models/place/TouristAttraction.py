from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Place import Place
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.intangible.Language import Language
from typing import Optional, Union, Dict, List, Any


class TouristAttraction(Place):
    """A tourist attraction.  In principle any Thing can be a [[TouristAttraction]], from a [[Mountain]] and [[LandmarksOrHistoricalBuildings]] to a [[LocalBusiness]].  This Type can be used on its own to describe a general [[TouristAttraction]], or be used as an [[additionalType]] to add tourist attraction properties to any other type.  (See examples below)"""
    type: str = field(default_factory=lambda: "TouristAttraction", name="@type")
    touristType: Union[List[Union[str, 'Audience']], Union[str, 'Audience'], None] = None
    availableLanguage: Union[List[Union[str, 'Language']], Union[str, 'Language'], None] = None