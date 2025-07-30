from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.MusicRecording import MusicRecording
    from msgspec_schemaorg.models.intangible.ItemList import ItemList
from typing import Optional, Union, Dict, List, Any


class MusicPlaylist(CreativeWork):
    """A collection of music tracks in playlist form."""
    type: str = field(default_factory=lambda: "MusicPlaylist", name="@type")
    tracks: Union[List['MusicRecording'], 'MusicRecording', None] = None
    track: Union[List[Union['MusicRecording', 'ItemList']], Union['MusicRecording', 'ItemList'], None] = None
    numTracks: Union[List[int], int, None] = None