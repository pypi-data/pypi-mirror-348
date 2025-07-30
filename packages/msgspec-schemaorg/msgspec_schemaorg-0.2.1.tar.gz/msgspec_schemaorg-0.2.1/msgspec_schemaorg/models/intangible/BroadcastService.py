from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Service import Service
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.BroadcastChannel import BroadcastChannel
    from msgspec_schemaorg.models.intangible.BroadcastFrequencySpecification import BroadcastFrequencySpecification
    from msgspec_schemaorg.models.intangible.BroadcastService import BroadcastService
    from msgspec_schemaorg.models.intangible.Language import Language
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.place.Place import Place
from typing import Optional, Union, Dict, List, Any


class BroadcastService(Service):
    """A delivery service through which content is provided via broadcast over the air or online."""
    type: str = field(default_factory=lambda: "BroadcastService", name="@type")
    broadcastAffiliateOf: Union[List['Organization'], 'Organization', None] = None
    area: Union[List['Place'], 'Place', None] = None
    broadcastTimezone: Union[List[str], str, None] = None
    broadcastDisplayName: Union[List[str], str, None] = None
    parentService: Union[List['BroadcastService'], 'BroadcastService', None] = None
    broadcastFrequency: Union[List[Union[str, 'BroadcastFrequencySpecification']], Union[str, 'BroadcastFrequencySpecification'], None] = None
    hasBroadcastChannel: Union[List['BroadcastChannel'], 'BroadcastChannel', None] = None
    inLanguage: Union[List[Union[str, 'Language']], Union[str, 'Language'], None] = None
    videoFormat: Union[List[str], str, None] = None
    broadcaster: Union[List['Organization'], 'Organization', None] = None
    callSign: Union[List[str], str, None] = None