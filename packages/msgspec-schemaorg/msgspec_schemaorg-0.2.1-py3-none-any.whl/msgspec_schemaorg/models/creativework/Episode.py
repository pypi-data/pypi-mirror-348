from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWorkSeason import CreativeWorkSeason
    from msgspec_schemaorg.models.creativework.CreativeWorkSeries import CreativeWorkSeries
    from msgspec_schemaorg.models.creativework.VideoObject import VideoObject
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.organization.MusicGroup import MusicGroup
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.organization.PerformingGroup import PerformingGroup
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class Episode(CreativeWork):
    """A media episode (e.g. TV, radio, video game) which can be part of a series or season."""
    type: str = field(default_factory=lambda: "Episode", name="@type")
    duration: Union[List[Union['QuantitativeValue', 'Duration']], Union['QuantitativeValue', 'Duration'], None] = None
    trailer: Union[List['VideoObject'], 'VideoObject', None] = None
    actor: Union[List[Union['PerformingGroup', 'Person']], Union['PerformingGroup', 'Person'], None] = None
    director: Union[List['Person'], 'Person', None] = None
    directors: Union[List['Person'], 'Person', None] = None
    episodeNumber: Union[List[Union[int, str]], Union[int, str], None] = None
    partOfSeries: Union[List['CreativeWorkSeries'], 'CreativeWorkSeries', None] = None
    musicBy: Union[List[Union['MusicGroup', 'Person']], Union['MusicGroup', 'Person'], None] = None
    partOfSeason: Union[List['CreativeWorkSeason'], 'CreativeWorkSeason', None] = None
    actors: Union[List['Person'], 'Person', None] = None
    productionCompany: Union[List['Organization'], 'Organization', None] = None