from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.BroadcastFrequencySpecification import BroadcastFrequencySpecification
    from msgspec_schemaorg.models.intangible.BroadcastService import BroadcastService
    from msgspec_schemaorg.models.intangible.CableOrSatelliteService import CableOrSatelliteService
from typing import Optional, Union, Dict, List, Any


class BroadcastChannel(Intangible):
    """A unique instance of a BroadcastService on a CableOrSatelliteService lineup."""
    type: str = field(default_factory=lambda: "BroadcastChannel", name="@type")
    inBroadcastLineup: Union[List['CableOrSatelliteService'], 'CableOrSatelliteService', None] = None
    broadcastFrequency: Union[List[Union[str, 'BroadcastFrequencySpecification']], Union[str, 'BroadcastFrequencySpecification'], None] = None
    broadcastServiceTier: Union[List[str], str, None] = None
    providesBroadcastService: Union[List['BroadcastService'], 'BroadcastService', None] = None
    broadcastChannelId: Union[List[str], str, None] = None
    genre: Union[List[Union['URL', str]], Union['URL', str], None] = None