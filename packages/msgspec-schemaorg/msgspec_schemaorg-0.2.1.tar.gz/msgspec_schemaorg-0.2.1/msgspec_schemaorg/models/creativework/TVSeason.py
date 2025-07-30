from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.TVSeries import TVSeries
    from msgspec_schemaorg.models.place.Country import Country
from typing import Optional, Union, Dict, List, Any


class TVSeason(CreativeWork):
    """Season dedicated to TV broadcast and associated online delivery."""
    type: str = field(default_factory=lambda: "TVSeason", name="@type")
    titleEIDR: Union[List[Union['URL', str]], Union['URL', str], None] = None
    countryOfOrigin: Union[List['Country'], 'Country', None] = None
    partOfTVSeries: Union[List['TVSeries'], 'TVSeries', None] = None