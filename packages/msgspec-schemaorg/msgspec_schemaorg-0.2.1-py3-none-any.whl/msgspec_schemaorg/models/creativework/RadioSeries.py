from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWorkSeries import CreativeWorkSeries
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWorkSeason import CreativeWorkSeason
    from msgspec_schemaorg.models.creativework.Episode import Episode
    from msgspec_schemaorg.models.creativework.VideoObject import VideoObject
    from msgspec_schemaorg.models.organization.MusicGroup import MusicGroup
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.organization.PerformingGroup import PerformingGroup
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class RadioSeries(CreativeWorkSeries):
    """CreativeWorkSeries dedicated to radio broadcast and associated online delivery."""
    type: str = field(default_factory=lambda: "RadioSeries", name="@type")
    episodes: Union[List['Episode'], 'Episode', None] = None
    trailer: Union[List['VideoObject'], 'VideoObject', None] = None
    actor: Union[List[Union['PerformingGroup', 'Person']], Union['PerformingGroup', 'Person'], None] = None
    season: Union[List[Union['URL', 'CreativeWorkSeason']], Union['URL', 'CreativeWorkSeason'], None] = None
    director: Union[List['Person'], 'Person', None] = None
    numberOfSeasons: Union[List[int], int, None] = None
    directors: Union[List['Person'], 'Person', None] = None
    episode: Union[List['Episode'], 'Episode', None] = None
    numberOfEpisodes: Union[List[int], int, None] = None
    musicBy: Union[List[Union['MusicGroup', 'Person']], Union['MusicGroup', 'Person'], None] = None
    containsSeason: Union[List['CreativeWorkSeason'], 'CreativeWorkSeason', None] = None
    actors: Union[List['Person'], 'Person', None] = None
    seasons: Union[List['CreativeWorkSeason'], 'CreativeWorkSeason', None] = None
    productionCompany: Union[List['Organization'], 'Organization', None] = None