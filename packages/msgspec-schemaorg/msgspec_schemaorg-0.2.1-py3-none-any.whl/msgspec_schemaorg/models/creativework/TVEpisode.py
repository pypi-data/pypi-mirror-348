from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Episode import Episode
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.TVSeries import TVSeries
    from msgspec_schemaorg.models.intangible.Language import Language
    from msgspec_schemaorg.models.place.Country import Country
from typing import Optional, Union, Dict, List, Any


class TVEpisode(Episode):
    """A TV episode which can be part of a series or season."""
    type: str = field(default_factory=lambda: "TVEpisode", name="@type")
    titleEIDR: Union[List[Union['URL', str]], Union['URL', str], None] = None
    countryOfOrigin: Union[List['Country'], 'Country', None] = None
    subtitleLanguage: Union[List[Union[str, 'Language']], Union[str, 'Language'], None] = None
    partOfTVSeries: Union[List['TVSeries'], 'TVSeries', None] = None