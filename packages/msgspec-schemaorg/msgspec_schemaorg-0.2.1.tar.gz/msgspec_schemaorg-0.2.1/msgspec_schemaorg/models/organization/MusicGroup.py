from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.PerformingGroup import PerformingGroup
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.MusicAlbum import MusicAlbum
    from msgspec_schemaorg.models.creativework.MusicRecording import MusicRecording
    from msgspec_schemaorg.models.intangible.ItemList import ItemList
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class MusicGroup(PerformingGroup):
    """A musical group, such as a band, an orchestra, or a choir. Can also be a solo musician."""
    type: str = field(default_factory=lambda: "MusicGroup", name="@type")
    musicGroupMember: Union[List['Person'], 'Person', None] = None
    tracks: Union[List['MusicRecording'], 'MusicRecording', None] = None
    album: Union[List['MusicAlbum'], 'MusicAlbum', None] = None
    track: Union[List[Union['MusicRecording', 'ItemList']], Union['MusicRecording', 'ItemList'], None] = None
    albums: Union[List['MusicAlbum'], 'MusicAlbum', None] = None
    genre: Union[List[Union['URL', str]], Union['URL', str], None] = None