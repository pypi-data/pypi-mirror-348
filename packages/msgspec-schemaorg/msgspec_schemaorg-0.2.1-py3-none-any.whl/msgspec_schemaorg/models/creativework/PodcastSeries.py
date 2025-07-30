from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWorkSeries import CreativeWorkSeries
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.DataFeed import DataFeed
    from msgspec_schemaorg.models.organization.PerformingGroup import PerformingGroup
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class PodcastSeries(CreativeWorkSeries):
    """A podcast is an episodic series of digital audio or video files which a user can download and listen to."""
    type: str = field(default_factory=lambda: "PodcastSeries", name="@type")
    actor: Union[List[Union['PerformingGroup', 'Person']], Union['PerformingGroup', 'Person'], None] = None
    webFeed: Union[List[Union['URL', 'DataFeed']], Union['URL', 'DataFeed'], None] = None