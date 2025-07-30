from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.PostalAddress import PostalAddress
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.place.Place import Place
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class Game(CreativeWork):
    """The Game type represents things which are games. These are typically rule-governed recreational activities, e.g. role-playing games in which players assume the role of characters in a fictional setting."""
    type: str = field(default_factory=lambda: "Game", name="@type")
    characterAttribute: Union[List['Thing'], 'Thing', None] = None
    numberOfPlayers: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    gameItem: Union[List['Thing'], 'Thing', None] = None
    gameLocation: Union[List[Union['URL', 'Place', 'PostalAddress']], Union['URL', 'Place', 'PostalAddress'], None] = None
    quest: Union[List['Thing'], 'Thing', None] = None