from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.MusicPlaylist import MusicPlaylist
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.MusicRelease import MusicRelease
    from msgspec_schemaorg.enums.intangible.MusicAlbumProductionType import MusicAlbumProductionType
    from msgspec_schemaorg.enums.intangible.MusicAlbumReleaseType import MusicAlbumReleaseType
    from msgspec_schemaorg.models.organization.MusicGroup import MusicGroup
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class MusicAlbum(MusicPlaylist):
    """A collection of music tracks."""
    type: str = field(default_factory=lambda: "MusicAlbum", name="@type")
    albumReleaseType: Union[List['MusicAlbumReleaseType'], 'MusicAlbumReleaseType', None] = None
    byArtist: Union[List[Union['MusicGroup', 'Person']], Union['MusicGroup', 'Person'], None] = None
    albumProductionType: Union[List['MusicAlbumProductionType'], 'MusicAlbumProductionType', None] = None
    albumRelease: Union[List['MusicRelease'], 'MusicRelease', None] = None