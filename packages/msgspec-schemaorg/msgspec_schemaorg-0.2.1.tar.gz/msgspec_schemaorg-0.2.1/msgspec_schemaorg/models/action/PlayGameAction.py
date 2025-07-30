from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.ConsumeAction import ConsumeAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.GameAvailabilityEnumeration import GameAvailabilityEnumeration
from typing import Optional, Union, Dict, List, Any


class PlayGameAction(ConsumeAction):
    """The act of playing a video game."""
    type: str = field(default_factory=lambda: "PlayGameAction", name="@type")
    gameAvailabilityType: Union[List[Union[str, 'GameAvailabilityEnumeration']], Union[str, 'GameAvailabilityEnumeration'], None] = None