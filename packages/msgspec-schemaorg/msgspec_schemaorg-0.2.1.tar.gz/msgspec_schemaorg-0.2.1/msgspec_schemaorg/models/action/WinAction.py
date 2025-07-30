from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.AchieveAction import AchieveAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class WinAction(AchieveAction):
    """The act of achieving victory in a competitive activity."""
    type: str = field(default_factory=lambda: "WinAction", name="@type")
    loser: Union[List['Person'], 'Person', None] = None