from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.VideoGame import VideoGame
    from msgspec_schemaorg.enums.intangible.GameServerStatus import GameServerStatus
from typing import Optional, Union, Dict, List, Any


class GameServer(Intangible):
    """Server that provides game interaction in a multiplayer game."""
    type: str = field(default_factory=lambda: "GameServer", name="@type")
    game: Union[List['VideoGame'], 'VideoGame', None] = None
    playersOnline: Union[List[int], int, None] = None
    serverStatus: Union[List['GameServerStatus'], 'GameServerStatus', None] = None