from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Game import Game
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.creativework.VideoObject import VideoObject
    from msgspec_schemaorg.enums.intangible.GamePlayMode import GamePlayMode
    from msgspec_schemaorg.models.intangible.GameServer import GameServer
    from msgspec_schemaorg.models.organization.MusicGroup import MusicGroup
    from msgspec_schemaorg.models.organization.PerformingGroup import PerformingGroup
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class VideoGame(Game):
    """A video game is an electronic game that involves human interaction with a user interface to generate visual feedback on a video device."""
    type: str = field(default_factory=lambda: "VideoGame", name="@type")
    cheatCode: Union[List['CreativeWork'], 'CreativeWork', None] = None
    trailer: Union[List['VideoObject'], 'VideoObject', None] = None
    actor: Union[List[Union['PerformingGroup', 'Person']], Union['PerformingGroup', 'Person'], None] = None
    gameServer: Union[List['GameServer'], 'GameServer', None] = None
    playMode: Union[List['GamePlayMode'], 'GamePlayMode', None] = None
    gameTip: Union[List['CreativeWork'], 'CreativeWork', None] = None
    director: Union[List['Person'], 'Person', None] = None
    directors: Union[List['Person'], 'Person', None] = None
    gamePlatform: Union[List[Union['URL', str, 'Thing']], Union['URL', str, 'Thing'], None] = None
    musicBy: Union[List[Union['MusicGroup', 'Person']], Union['MusicGroup', 'Person'], None] = None
    gameEdition: Union[List[str], str, None] = None
    actors: Union[List['Person'], 'Person', None] = None