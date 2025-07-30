from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.action.Action import Action
    from msgspec_schemaorg.models.creativework.SoftwareApplication import SoftwareApplication
    from msgspec_schemaorg.models.creativework.WebSite import WebSite
    from msgspec_schemaorg.models.intangible.PostalAddress import PostalAddress
    from msgspec_schemaorg.models.intangible.VirtualLocation import VirtualLocation
    from msgspec_schemaorg.models.place.Place import Place
from datetime import datetime, time
from typing import Optional, Union, Dict, List, Any


class InteractionCounter(StructuredValue):
    """A summary of how users have interacted with this CreativeWork. In most cases, authors will use a subtype to specify the specific type of interaction."""
    type: str = field(default_factory=lambda: "InteractionCounter", name="@type")
    startTime: Union[List[Union[datetime, time]], Union[datetime, time], None] = None
    interactionService: Union[List[Union['WebSite', 'SoftwareApplication']], Union['WebSite', 'SoftwareApplication'], None] = None
    userInteractionCount: Union[List[int], int, None] = None
    location: Union[List[Union[str, 'VirtualLocation', 'PostalAddress', 'Place']], Union[str, 'VirtualLocation', 'PostalAddress', 'Place'], None] = None
    endTime: Union[List[Union[datetime, time]], Union[datetime, time], None] = None
    interactionType: Union[List['Action'], 'Action', None] = None