from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWorkSeries import CreativeWorkSeries
    from msgspec_schemaorg.models.creativework.Episode import Episode
    from msgspec_schemaorg.models.creativework.VideoObject import VideoObject
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.organization.PerformingGroup import PerformingGroup
    from msgspec_schemaorg.models.person.Person import Person
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class CreativeWorkSeason(CreativeWork):
    """A media season, e.g. TV, radio, video game etc."""
    type: str = field(default_factory=lambda: "CreativeWorkSeason", name="@type")
    episodes: Union[List['Episode'], 'Episode', None] = None
    trailer: Union[List['VideoObject'], 'VideoObject', None] = None
    actor: Union[List[Union['PerformingGroup', 'Person']], Union['PerformingGroup', 'Person'], None] = None
    director: Union[List['Person'], 'Person', None] = None
    endDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    seasonNumber: Union[List[Union[int, str]], Union[int, str], None] = None
    episode: Union[List['Episode'], 'Episode', None] = None
    partOfSeries: Union[List['CreativeWorkSeries'], 'CreativeWorkSeries', None] = None
    numberOfEpisodes: Union[List[int], int, None] = None
    startDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    productionCompany: Union[List['Organization'], 'Organization', None] = None